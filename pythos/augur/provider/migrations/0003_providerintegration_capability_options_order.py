# Generated by Django 5.1 on 2024-09-06 17:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_integrationcapabilityoption'),
        ('provider', '0002_delete_configoption_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='providerintegration',
            name='capability_options',
            field=models.ManyToManyField(to='core.integrationcapabilityoption'),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(auto_now=True, db_index=True)),
                ('name', models.CharField(blank=True, default='', max_length=256)),
                ('external_id', models.CharField(blank=True, default='', max_length=512)),
                ('status', models.CharField(blank=True, choices=[('INITIALIZED', 'Initialized'), ('ORDERED', 'Ordered'), ('COMPLETED', 'Completed'), ('FAILED', 'Failed')], default='INITIALIZED', max_length=128)),
                ('provider_integration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='provider.providerintegration')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
