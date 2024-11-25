from django.urls import path
from . import views

urlpatterns = [
    path("", views.all_controls, name="control_list"),
    path(
        "add_validacion_diseno/<control_id>",
        views.add_validacion_diseño,
        name="add_validacion_diseno",
    ),
    path(
        "add_encabezado_control/<control_id>",
        views.add_encabezado_control,
        name="add_encabezado_control",
    ),
    path("control/<control_id>", views.control_by_id, name="control"),
]
