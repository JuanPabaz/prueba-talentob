from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Auditor(models.Model):
    nombre_completo = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100, null=True, blank=True)
    area = models.CharField(max_length=100, null=True, blank=True)
    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="usuarios", blank=True
    )

    def __str__(self):
        return self.nombre_completo


class Control(models.Model):
    CICLOS = [
        ("Semestre 1", "Semestre 1"),
        ("Semestre 2", "Semestre 2"),
    ]
    PRIORIDADES = [
        ("Baja", "Baja"),
        ("Media", "Media"),
        ("Alta", "Alta"),
    ]

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    ciclo = models.CharField(max_length=15, choices=CICLOS)
    año = models.PositiveIntegerField()
    codigo = models.CharField(max_length=100)
    tipologia = models.CharField(max_length=100)
    frecuencia = models.CharField(max_length=100)
    objetivo = models.CharField(max_length=150)
    clasificacion = models.CharField(max_length=150)
    prioridad = models.CharField(max_length=20, choices=PRIORIDADES)
    auditor = models.ForeignKey(
        Auditor, on_delete=models.CASCADE, related_name="controles"
    )

    def __str__(self):
        return self.nombre


class ValidacionDiseño(models.Model):
    control = models.OneToOneField(
        Control, on_delete=models.CASCADE, related_name="validacion"
    )
    fecha_ejecucion = models.DateField()
    nombre_ejecutor = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100, null=True, blank=True)
    area = models.CharField(max_length=100, null=True, blank=True)
    comentarios = models.TextField(null=True, blank=True)
    conclusion = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Validación de {self.control.nombre} - {self.fecha_ejecucion}"


class Pregunta(models.Model):
    texto = models.TextField()

    def __str__(self):
        return self.texto


class Respuesta(models.Model):
    validacion = models.ForeignKey(
        ValidacionDiseño, on_delete=models.CASCADE, related_name="respuestas"
    )
    pregunta = models.ForeignKey(
        Pregunta, on_delete=models.CASCADE, related_name="respuestas"
    )
    respuesta = models.CharField(max_length=100, null=True, blank=True)
    explicacion = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return f"Respuesta a '{self.pregunta.texto}'"


class Encabezado(models.Model):
    ESTADOS = [
        ("Sin iniciar", "Sin iniciar"),
        ("En Proceso", "En Proceso"),
        ("Terminado", "Terminado"),
        ("No evaluado", "No evaluado"),
    ]

    control = models.OneToOneField(
        Control, on_delete=models.CASCADE, related_name="encabezado"
    )
    fecha = models.DateField(null=True, blank=True)
    horas_totales = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    estado = models.CharField(max_length=20, choices=ESTADOS)
    respuesta = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return f"Encabezado de {self.control.nombre}"
