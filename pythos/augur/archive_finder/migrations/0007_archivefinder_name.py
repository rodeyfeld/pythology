# Generated by Django 5.1 on 2024-10-13 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive_finder', '0006_archiveresult_thumbnail'),
    ]

    operations = [
        migrations.AddField(
            model_name='archivefinder',
            name='name',
            field=models.CharField(blank=True, default='', max_length=256),
        ),
    ]
