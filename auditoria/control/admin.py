from django.contrib import admin
from .models import Control, ValidacionDiseño, Respuesta, Pregunta, Auditor
# Register your models here.

admin.site.register(ValidacionDiseño)
admin.site.register(Respuesta)
admin.site.register(Pregunta)
admin.site.register(Auditor)

@admin.register(Control)
class ControlAdmin(admin.ModelAdmin):
    list_display = ('nombre','descripcion','ciclo','año','auditor')
    ordering = ('nombre',)
    search_fields = ('nombre','ciclo')