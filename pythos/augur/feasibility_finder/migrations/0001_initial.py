# Generated by Django 5.1 on 2024-09-01 04:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        ('provider', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeasibilityFinder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(auto_now=True, db_index=True)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('imagery_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.imageryrequest')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FeasibilityResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(auto_now=True, db_index=True)),
                ('confidence_score', models.FloatField()),
                ('feasibility_finder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feasibility_finder.feasibilityfinder')),
                ('provider_integration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='provider.providerintegration')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
