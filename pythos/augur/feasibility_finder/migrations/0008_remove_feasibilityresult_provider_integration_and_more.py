# Generated by Django 5.1 on 2024-10-04 05:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feasibility_finder', '0007_feasibilityorder'),
        ('provider', '0003_providerintegration_capability_options_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feasibilityresult',
            name='provider_integration',
        ),
        migrations.AddField(
            model_name='feasibilityresult',
            name='provider',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='provider.provider'),
            preserve_default=False,
        ),
    ]
