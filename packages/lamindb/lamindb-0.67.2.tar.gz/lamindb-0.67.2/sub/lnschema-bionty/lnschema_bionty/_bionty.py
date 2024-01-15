from typing import Dict, Optional, Union

import bionty as bt
from django.core.exceptions import ObjectDoesNotExist
from lamin_utils import logger
from lnschema_core.models import Registry  # TODO: import Registry instead of ORM

from . import ids


def create_or_get_organism_record(organism: Optional[Union[str, Registry]], orm: Registry) -> Optional[Registry]:
    # return None if an Registry doesn't have organism field
    organism_record = None
    if hasattr(orm, "organism"):
        # using global setting of organism
        from .dev._settings import settings

        if organism is None and settings.organism is not None:
            logger.debug(f"using global setting organism = {settings.organism.name}")
            return settings.organism

        if isinstance(organism, Registry):
            organism_record = organism
        elif isinstance(organism, str):
            from lnschema_bionty import Organism

            try:
                # existing organism record
                organism_record = Organism.objects.get(name=organism)
            except ObjectDoesNotExist:
                try:
                    # create a organism record from bionty reference
                    organism_record = Organism.from_public(name=organism)
                    # link the organism record to the default bionty source
                    organism_record.public_source = get_public_source_record(bt.Organism())  # type:ignore
                    organism_record.save()  # type:ignore
                except KeyError:
                    # no such organism is found in bionty reference
                    organism_record = None

        if organism_record is None:
            raise AssertionError(f"{orm.__name__} requires to specify a organism name via `organism=` or `lb.settings.organism=`!")

    return organism_record


def get_public_source_record(public_ontology: bt.PublicOntology):
    kwargs = dict(
        entity=public_ontology.__class__.__name__,
        organism=public_ontology.organism,
        source=public_ontology.source,
        version=public_ontology.version,
    )
    from .models import PublicSource

    source_record = PublicSource.objects.filter(**kwargs).get()
    return source_record


def encode_uid(orm: Registry, kwargs: dict):
    if kwargs.get("uid") is not None:
        # if uid is passed, no encoding is needed
        return kwargs
    try:
        name = orm.__name__.lower()
    except AttributeError:
        name = orm.__class__.__name__.lower()
    ontology = False
    str_to_encode = None
    if name == "gene":
        str_to_encode = kwargs.get("ensembl_gene_id")
        if str_to_encode is None or str_to_encode == "":
            str_to_encode = kwargs.get("stable_id")
        if str_to_encode is None or str_to_encode == "":
            str_to_encode = kwargs.get("symbol")
        if str_to_encode is None or str_to_encode == "":
            raise AssertionError("must provide ensembl_gene_id, stable_id or symbol")
    elif name == "protein":
        str_to_encode = kwargs.get("uniprotkb_id")
        if str_to_encode is None or str_to_encode == "":
            str_to_encode = kwargs.get("name")
        if str_to_encode is None or str_to_encode == "":
            raise AssertionError("must provide uniprotkb_id or name")
    elif name == "cellmarker":
        str_to_encode = kwargs.get("name")
        if str_to_encode is None or str_to_encode == "":
            raise AssertionError("must provide name")
    elif name == "publicsource":
        str_to_encode = f'{kwargs.get("entity", "")}{kwargs.get("source", "")}{kwargs.get("organism", "")}{kwargs.get("version", "")}'  # noqa
    else:
        str_to_encode = kwargs.get("ontology_id")
        if str_to_encode is None or str_to_encode == "":
            str_to_encode = kwargs.get("name")
        if str_to_encode is None or str_to_encode == "":
            raise AssertionError("must provide ontology_id or name")
        ontology = True

    if str_to_encode is not None and len(str_to_encode) > 0:
        if ontology:
            id_encoder = ids.ontology
        else:
            try:
                id_encoder = getattr(ids, name)
            except Exception:
                return kwargs
        kwargs["uid"] = id_encoder(str_to_encode)
    return kwargs


def lookup2kwargs(orm: Registry, *args, **kwargs) -> Dict:
    """Pass bionty search/lookup results."""
    arg = args[0]
    if isinstance(arg, tuple):
        bionty_kwargs = arg._asdict()  # type:ignore
    else:
        bionty_kwargs = arg[0]._asdict()

    if len(bionty_kwargs) > 0:
        import bionty as bt

        # add organism and public_source
        organism_record = create_or_get_organism_record(orm=orm.__class__, organism=kwargs.get("organism"))
        if organism_record is not None:
            bionty_kwargs["organism"] = organism_record
        public_ontology = getattr(bt, orm.__class__.__name__)(organism=organism_record.name if organism_record is not None else None)
        bionty_kwargs["public_source"] = get_public_source_record(public_ontology)

        model_field_names = {i.name for i in orm._meta.fields}
        model_field_names.add("parents")
        bionty_kwargs = {k: v for k, v in bionty_kwargs.items() if k in model_field_names}
    return encode_uid(orm=orm, kwargs=bionty_kwargs)


# backward compat
create_or_get_species_record = create_or_get_organism_record
