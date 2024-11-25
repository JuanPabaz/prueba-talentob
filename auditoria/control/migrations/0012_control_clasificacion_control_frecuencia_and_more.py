# Generated by Django 5.1.3 on 2024-11-25 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0011_remove_control_clasificacion_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='control',
            name='clasificacion',
            field=models.CharField(default='Automatico', max_length=150),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='control',
            name='frecuencia',
            field=models.CharField(default='Mensual', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='control',
            name='objetivo',
            field=models.CharField(default='Grantizar la integridad y la exactitud de la informacion....', max_length=150),
            preserve_default=False,
        ),
    ]
