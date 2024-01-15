# Generated by Django 4.2.5 on 2023-12-12 19:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("lnschema_core", "0032_remove_dataset_storage"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="artifact",
            unique_together=set(),
        ),
        migrations.AddField(
            model_name="artifact",
            name="n_objects",
            field=models.BigIntegerField(db_index=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="artifact",
            name="n_observations",
            field=models.BigIntegerField(db_index=True, default=None, null=True),
        ),
    ]
