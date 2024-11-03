# Generated by Django 5.1 on 2024-11-03 16:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive_finder', '0007_archivefinder_name'),
        ('augury', '0002_archiveitem_metadata'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='archiveresult',
            name='archive_finder',
        ),
        migrations.CreateModel(
            name='ArchiveLookup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(auto_now=True, db_index=True)),
                ('archive_finder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='archive_finder.archivefinder')),
                ('archive_items', models.ManyToManyField(to='augury.archiveitem')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='archiveresult',
            name='archive_lookup',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='archive_finder.archivelookup'),
        ),
    ]
