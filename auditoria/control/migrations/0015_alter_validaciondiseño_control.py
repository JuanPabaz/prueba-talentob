# Generated by Django 5.1.3 on 2024-11-25 16:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0014_remove_encabezado_fin_remove_encabezado_inicio_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='validaciondiseño',
            name='control',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='validacion', to='control.control'),
        ),
    ]
