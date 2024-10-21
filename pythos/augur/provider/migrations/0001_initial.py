# Generated by Django 5.1 on 2024-09-01 04:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConfigOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(auto_now=True, db_index=True)),
                ('key', models.CharField(choices=[('username', 'Username'), ('password', 'Password'), ('api_key', 'Api Key'), ('client_id', 'Client Id'), ('client_secret', 'Client Secret'), ('token_refresh_endpoint', 'Token Refresh Endpoint'), ('auth_endpoint', 'Auth Endpoint'), ('task_endpoint', 'Task Endpoint'), ('collect_endpoint', 'Collect Endpoint'), ('stac_endpoint', 'Stac Endpoint')], max_length=512)),
                ('value', models.CharField(max_length=4096)),
                ('is_secret', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(auto_now=True, db_index=True)),
                ('name', models.CharField(max_length=256)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProviderIntegration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(auto_now=True, db_index=True)),
                ('name', models.CharField(max_length=256)),
                ('is_active', models.BooleanField(default=True)),
                ('config_options', models.ManyToManyField(to='provider.configoption')),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='provider.provider')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
