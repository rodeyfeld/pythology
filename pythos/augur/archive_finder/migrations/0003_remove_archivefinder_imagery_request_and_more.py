# Generated by Django 5.1 on 2024-10-03 23:23

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('archive_finder', '0002_archiveorder'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='archivefinder',
            name='imagery_request',
        ),
        migrations.AddField(
            model_name='archivefinder',
            name='geometry',
            field=django.contrib.gis.db.models.fields.GeometryField(default=None, srid=4326),
            preserve_default=False,
        ),
    ]
