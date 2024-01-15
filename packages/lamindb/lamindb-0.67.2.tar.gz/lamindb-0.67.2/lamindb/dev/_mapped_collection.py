from collections import Counter
from functools import reduce
from os import PathLike
from typing import List, Literal, Optional, Union

import numpy as np
import pandas as pd
from lamin_utils import logger
from lamindb_setup.dev.upath import UPath

from .storage._backed_access import (
    ArrayTypes,
    GroupTypes,
    StorageType,
    _safer_read_index,
    registry,
)


class _Connect:
    def __init__(self, storage):
        if isinstance(storage, UPath):
            self.conn, self.store = registry.open("h5py", storage)
            self.to_close = True
        else:
            self.conn, self.store = None, storage
            self.to_close = False

    def __enter__(self):
        return self.store

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        if not self.to_close:
            return
        if hasattr(self.store, "close"):
            self.store.close()
        if hasattr(self.conn, "close"):
            self.conn.close()


class MappedCollection:
    """Map-style collection for use in data loaders.

    This currently only works for collections of `AnnData` objects.

    For an example, see :meth:`~lamindb.Collection.mapped`.

    .. note::

        A similar data loader exists `here
        <https://github.com/Genentech/scimilarity>`__.
    """

    def __init__(
        self,
        path_list: List[Union[str, PathLike]],
        label_keys: Optional[Union[str, List[str]]] = None,
        join: Optional[Literal["inner", "outer"]] = "inner",
        encode_labels: bool = True,
        cache_categories: bool = True,
        parallel: bool = False,
        dtype: Optional[str] = None,
    ):
        assert join in {None, "inner", "outer"}

        self.storages = []  # type: ignore
        self.conns = []  # type: ignore
        self.parallel = parallel
        self._make_connections(path_list, parallel)

        self.n_obs_list = []
        for storage in self.storages:
            with _Connect(storage) as store:
                X = store["X"]
                if isinstance(X, ArrayTypes):  # type: ignore
                    self.n_obs_list.append(X.shape[0])
                else:
                    self.n_obs_list.append(X.attrs["shape"][0])
        self.n_obs = sum(self.n_obs_list)

        self.indices = np.hstack([np.arange(n_obs) for n_obs in self.n_obs_list])
        self.storage_idx = np.repeat(np.arange(len(self.storages)), self.n_obs_list)

        self.join_vars = join
        self.var_indices = None
        if self.join_vars is not None:
            self._make_join_vars()

        self.encode_labels = encode_labels
        self.label_keys = [label_keys] if isinstance(label_keys, str) else label_keys
        if self.label_keys is not None:
            if cache_categories:
                self._cache_categories(self.label_keys)
            else:
                self._cache_cats: dict = {}
            if self.encode_labels:
                self._make_encoders(self.label_keys)

        self._dtype = dtype
        self._closed = False

    def _make_connections(self, path_list: list, parallel: bool):
        for path in path_list:
            path = UPath(path)
            if path.exists() and path.is_file():  # type: ignore
                if parallel:
                    conn, storage = None, path
                else:
                    conn, storage = registry.open("h5py", path)
            else:
                conn, storage = registry.open("zarr", path)
            self.conns.append(conn)
            self.storages.append(storage)

    def _cache_categories(self, label_keys: list):
        self._cache_cats = {}
        decode = np.frompyfunc(lambda x: x.decode("utf-8"), 1, 1)
        for label in label_keys:
            self._cache_cats[label] = []
            for storage in self.storages:
                with _Connect(storage) as store:
                    cats = self.get_categories(store, label)
                    if cats is not None:
                        cats = decode(cats) if isinstance(cats[0], bytes) else cats[...]
                    self._cache_cats[label].append(cats)

    def _make_encoders(self, label_keys: list):
        self.encoders = []
        for label in label_keys:
            cats = self.get_merged_categories(label)
            self.encoders.append({cat: i for i, cat in enumerate(cats)})

    def _make_join_vars(self):
        var_list = []
        for storage in self.storages:
            with _Connect(storage) as store:
                var_list.append(_safer_read_index(store["var"]))

        self.var_joint = None
        vars_eq = all(var_list[0].equals(vrs) for vrs in var_list[1:])
        if vars_eq:
            self.join_vars = None
            self.var_joint = var_list[0]
            return

        if self.join_vars == "inner":
            self.var_joint = reduce(pd.Index.intersection, var_list)
            if len(self.var_joint) == 0:
                raise ValueError(
                    "The provided AnnData objects don't have shared varibales.\n"
                    "Use join='outer'."
                )
            self.var_indices = [vrs.get_indexer(self.var_joint) for vrs in var_list]
        elif self.join_vars == "outer":
            self.var_joint = reduce(pd.Index.union, var_list)
            self.var_indices = [self.var_joint.get_indexer(vrs) for vrs in var_list]

    def __len__(self):
        return self.n_obs

    def __getitem__(self, idx: int):
        obs_idx = self.indices[idx]
        storage_idx = self.storage_idx[idx]
        if self.var_indices is not None:
            var_idxs_join = self.var_indices[storage_idx]
        else:
            var_idxs_join = None

        with _Connect(self.storages[storage_idx]) as store:
            out = [self.get_data_idx(store, obs_idx, var_idxs_join)]
            if self.label_keys is not None:
                for i, label in enumerate(self.label_keys):
                    if label in self._cache_cats:
                        cats = self._cache_cats[label][storage_idx]
                        if cats is None:
                            cats = []
                    else:
                        cats = None
                    label_idx = self.get_label_idx(store, obs_idx, label, cats)
                    if self.encode_labels:
                        label_idx = self.encoders[i][label_idx]
                    out.append(label_idx)
        return out

    def get_data_idx(
        self,
        storage: StorageType,  # type: ignore
        idx: int,
        var_idxs_join: Optional[list] = None,
        layer_key: Optional[str] = None,
    ):
        """Get the index for the data."""
        layer = storage["X"] if layer_key is None else storage["layers"][layer_key]  # type: ignore
        if isinstance(layer, ArrayTypes):  # type: ignore
            layer_idx = layer[idx]
            if self.join_vars is None:
                result = layer_idx
                if self._dtype is not None:
                    result = result.astype(self._dtype, copy=False)
            elif self.join_vars == "outer":
                dtype = layer_idx.dtype if self._dtype is None else self._dtype
                result = np.zeros(len(self.var_joint), dtype=dtype)
                result[var_idxs_join] = layer_idx
            else:  # inner join
                result = layer_idx[var_idxs_join]
                if self._dtype is not None:
                    result = result.astype(self._dtype, copy=False)
            return result
        else:  # assume csr_matrix here
            data = layer["data"]
            indices = layer["indices"]
            indptr = layer["indptr"]
            s = slice(*(indptr[idx : idx + 2]))
            data_s = data[s]
            dtype = data_s.dtype if self._dtype is None else self._dtype
            if self.join_vars == "outer":
                layer_idx = np.zeros(len(self.var_joint), dtype=dtype)
                layer_idx[var_idxs_join[indices[s]]] = data_s
            else:
                layer_idx = np.zeros(layer.attrs["shape"][1], dtype=dtype)
                layer_idx[indices[s]] = data_s
                if self.join_vars == "inner":
                    layer_idx = layer_idx[var_idxs_join]
            return layer_idx

    def get_label_idx(
        self,
        storage: StorageType,
        idx: int,
        label_key: str,
        categories: Optional[list] = None,
    ):
        """Get the index for the label by key."""
        obs = storage["obs"]  # type: ignore
        # how backwards compatible do we want to be here actually?
        if isinstance(obs, ArrayTypes):  # type: ignore
            label = obs[idx][obs.dtype.names.index(label_key)]
        else:
            labels = obs[label_key]
            if isinstance(labels, ArrayTypes):  # type: ignore
                label = labels[idx]
            else:
                label = labels["codes"][idx]
        if categories is not None:
            cats = categories
        else:
            cats = self.get_categories(storage, label_key)
        if cats is not None and len(cats) > 0:
            label = cats[label]
        if isinstance(label, bytes):
            label = label.decode("utf-8")
        return label

    def get_label_weights(self, label_keys: Union[str, List[str]]):
        """Get all weights for the given label keys."""
        if isinstance(label_keys, str):
            label_keys = [label_keys]
        labels_list = []
        for label_key in label_keys:
            labels_to_str = self.get_merged_labels(label_key).astype(str).astype("O")
            labels_list.append(labels_to_str)
        if len(labels_list) > 1:
            labels = reduce(lambda a, b: a + b, labels_list)
        else:
            labels = labels_list[0]
        labels = self.get_merged_labels(label_key)
        counter = Counter(labels)  # type: ignore
        weights = 1.0 / np.array([counter[label] for label in labels])
        return weights

    def get_merged_labels(self, label_key: str):
        """Get merged labels."""
        labels_merge = []
        decode = np.frompyfunc(lambda x: x.decode("utf-8"), 1, 1)
        for i, storage in enumerate(self.storages):
            with _Connect(storage) as store:
                codes = self.get_codes(store, label_key)
                labels = decode(codes) if isinstance(codes[0], bytes) else codes
                if label_key in self._cache_cats:
                    cats = self._cache_cats[label_key][i]
                else:
                    cats = self.get_categories(store, label_key)
                if cats is not None:
                    cats = decode(cats) if isinstance(cats[0], bytes) else cats
                    labels = cats[labels]
                labels_merge.append(labels)
        return np.hstack(labels_merge)

    def get_merged_categories(self, label_key: str):
        """Get merged categories."""
        cats_merge = set()
        decode = np.frompyfunc(lambda x: x.decode("utf-8"), 1, 1)
        for i, storage in enumerate(self.storages):
            with _Connect(storage) as store:
                if label_key in self._cache_cats:
                    cats = self._cache_cats[label_key][i]
                else:
                    cats = self.get_categories(store, label_key)
                if cats is not None:
                    cats = decode(cats) if isinstance(cats[0], bytes) else cats
                    cats_merge.update(cats)
                else:
                    codes = self.get_codes(store, label_key)
                    codes = decode(codes) if isinstance(codes[0], bytes) else codes
                    cats_merge.update(codes)
        return cats_merge

    def get_categories(self, storage: StorageType, label_key: str):  # type: ignore
        """Get categories."""
        obs = storage["obs"]  # type: ignore
        if isinstance(obs, ArrayTypes):  # type: ignore
            cat_key_uns = f"{label_key}_categories"
            if cat_key_uns in storage["uns"]:  # type: ignore
                return storage["uns"][cat_key_uns]  # type: ignore
            else:
                return None
        else:
            if "__categories" in obs:
                cats = obs["__categories"]
                if label_key in cats:
                    return cats[label_key]
                else:
                    return None
            labels = obs[label_key]
            if isinstance(labels, GroupTypes):  # type: ignore
                if "categories" in labels:
                    return labels["categories"]
                else:
                    return None
            else:
                if "categories" in labels.attrs:
                    return labels.attrs["categories"]
                else:
                    return None
        return None

    def get_codes(self, storage: StorageType, label_key: str):  # type: ignore
        """Get codes."""
        obs = storage["obs"]  # type: ignore
        if isinstance(obs, ArrayTypes):  # type: ignore
            label = obs[label_key]
        else:
            label = obs[label_key]
            if isinstance(label, ArrayTypes):  # type: ignore
                return label[...]
            else:
                return label["codes"][...]

    def close(self):
        """Close connection to array streaming backend."""
        for storage in self.storages:
            if hasattr(storage, "close"):
                storage.close()
        for conn in self.conns:
            if hasattr(conn, "close"):
                conn.close()
        self._closed = True

    @property
    def closed(self):
        return self._closed

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
