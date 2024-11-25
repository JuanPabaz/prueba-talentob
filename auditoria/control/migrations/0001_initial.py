# Generated by Django 5.1.3 on 2024-11-24 21:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Auditor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_completo', models.CharField(max_length=100)),
                ('cargo', models.CharField(blank=True, max_length=100, null=True)),
                ('area', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pregunta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50, unique=True)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('contraseña', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Control',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('ciclo', models.CharField(choices=[('Semestre 1', 'Semestre 1'), ('Semestre 2', 'Semestre 2')], max_length=15)),
                ('año', models.PositiveIntegerField()),
                ('auditor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='controles', to='control.auditor')),
            ],
        ),
        migrations.CreateModel(
            name='Encabezado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inicio', models.DateTimeField(blank=True, null=True)),
                ('fin', models.DateTimeField(blank=True, null=True)),
                ('horas_totales', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('estado', models.CharField(choices=[('En Proceso', 'En Proceso'), ('Terminado', 'Terminado')], max_length=20)),
                ('control', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='encabezado', to='control.control')),
            ],
        ),
        migrations.CreateModel(
            name='ValidacionDiseño',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_ejecucion', models.DateTimeField()),
                ('nombre_ejecutor', models.CharField(max_length=100)),
                ('cargo', models.CharField(blank=True, max_length=100, null=True)),
                ('area', models.CharField(blank=True, max_length=100, null=True)),
                ('comentarios', models.TextField(blank=True, null=True)),
                ('control', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='validaciones', to='control.control')),
            ],
        ),
        migrations.CreateModel(
            name='Respuesta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('respuesta', models.CharField(blank=True, max_length=100, null=True)),
                ('pregunta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='respuestas', to='control.pregunta')),
                ('validacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='respuestas', to='control.validaciondiseño')),
            ],
        ),
    ]
