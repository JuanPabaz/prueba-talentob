from django import forms
from django.forms import ModelForm
from .models import Encabezado, ValidacionDiseño


# Create validacion diseño
class ValidacionDiseñoForm(ModelForm):
    class Meta:
        model = ValidacionDiseño
        fields = ["fecha_ejecucion", "nombre_ejecutor", "cargo", "area", "comentarios"]
        widgets = {
            "control": forms.Select(
                attrs={
                    "class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                }
            ),
            "fecha_ejecucion": forms.DateInput(
                attrs={
                    "class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline",
                    "type": "date",
                }
            ),
            "nombre_ejecutor": forms.TextInput(
                attrs={
                    "class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                }
            ),
            "cargo": forms.TextInput(
                attrs={
                    "class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                }
            ),
            "area": forms.TextInput(
                attrs={
                    "class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                }
            ),
            "comentarios": forms.Textarea(
                attrs={
                    "class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                }
            ),
        }


class EncabezadoControlForm(ModelForm):
    class Meta:
        model = Encabezado
        fields = ["fecha", "horas_totales", "estado", "respuesta"]
        widgets = {
            "fecha": forms.DateInput(
                attrs={
                    "class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline",
                    "type": "date",
                }
            ),
            "horas_totales": forms.NumberInput(
                attrs={
                    "class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline",
                    "step": "0.01",
                }
            ),
            "estado": forms.Select(
                choices=Encabezado.ESTADOS,
                attrs={
                    "class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                },
            ),
            "respuesta": forms.TextInput(
                attrs={
                    "class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                }
            ),
        }
