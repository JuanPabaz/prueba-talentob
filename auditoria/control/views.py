from django.shortcuts import get_object_or_404, render
from .models import Control, Auditor, Encabezado, Pregunta, Respuesta, ValidacionDiseño
from .forms import EncabezadoControlForm, ValidacionDiseñoForm
from django.http import Http404, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required(login_url="login_user")
def all_controls(request):
    ano = request.session.get("ano", None)
    testing = request.session.get("testing", None)
    usuario_id = request.session.get("user_id", None)
    auditor = get_object_or_404(Auditor, usuario_id=usuario_id)
    control_list = Control.objects.filter(auditor=auditor, año=ano, ciclo=testing)

    data = []
    for control in control_list:
        encabezado = getattr(control, "encabezado", None)
        validacion = getattr(control, "validacion", None)

        control_data = {
            "id_control": control.id,
            "nombre_control": control.nombre,
            "codigo_control": control.codigo,
            "auditor": control.auditor.nombre_completo,
            "estado": encabezado.estado if encabezado else None,
            "conclusion": validacion.conclusion if validacion else None,
            "diseño": validacion.conclusion if validacion else None,
            "prioridad": control.prioridad,
        }

        data.append(control_data)
    return render(request, "control/control_list.html", {"data": data})


@login_required(login_url="login_user")
def add_validacion_diseño(request, control_id):
    control = Control.objects.get(pk=control_id)
    preguntas_list = Pregunta.objects.all()
    submitted = False
    validacion = validate_existing_validacion_diseño(control)
    if request.method == "POST":
        if validacion:
            form = ValidacionDiseñoForm(request.POST, instance=validacion)
        else:
            form = ValidacionDiseñoForm(request.POST)
        if form.is_valid():
            validacion = form.save(commit=False)
            validacion.control = control
            respuestas_completas = validate_all_respuestas(preguntas_list, request)
            if respuestas_completas is None:
                validacion.conclusion = "No Evaluado"
                validacion.save()
                messages.success(
                    request,
                    ("Evalución guardada con éxito."),
                )
                return HttpResponseRedirect("/control")
            elif not respuestas_completas:
                messages.success(
                    request,
                    (
                        "Faltan campos por diligenciar. Asegúrese de responder todas las preguntas."
                    ),
                )
                return render(
                    request,
                    "control/add_validacion_diseño.html",
                    {
                        "form": form,
                        "control": control,
                        "preguntas": preguntas_list,
                    },
                )

            validacion.save()
            save_respuestas(preguntas_list, request, validacion)
            grade_validacion(validacion)
            messages.success(
                request,
                ("Evalución guardada con éxito."),
            )
            return HttpResponseRedirect("/control")
    else:
        form = (
            ValidacionDiseñoForm(instance=validacion)
            if validacion
            else ValidacionDiseñoForm()
        )
        if "submitted" in request.GET:
            submitted = True
    return render(
        request,
        "control/add_validacion_diseño.html",
        {
            "form": form,
            "submitted": submitted,
            "control": control,
            "preguntas": preguntas_list,
        },
    )


def validate_existing_validacion_diseño(control):
    try:
        return control.validacion
    except ValidacionDiseño.DoesNotExist:
        return None


def save_respuestas(preguntas_list, request, validacion):
    for pregunta in preguntas_list:
        respuesta = request.POST.get(f"respuesta_{pregunta.id}")
        explicacion = request.POST.get(f"explicacion_{pregunta.id}")

        if respuesta:
            Respuesta.objects.create(
                validacion=validacion,
                pregunta=pregunta,
                respuesta=respuesta,
                explicacion=explicacion,
            )


def validate_all_respuestas(preguntas_list, request):
    any_answered = False
    all_answered = True

    for pregunta in preguntas_list:
        respuesta = request.POST.get(f"respuesta_{pregunta.id}")
        explicacion = request.POST.get(f"explicacion_{pregunta.id}")
        if respuesta and explicacion:
            any_answered = True
        else:
            all_answered = False

    if not any_answered:
        return None
    if not all_answered:
        return False
    return True


def grade_validacion(validacion):
    respuestas = Respuesta.objects.filter(validacion=validacion)

    if (
        respuestas.filter(respuesta="no").exists()
        or respuestas.filter(respuesta="no aplica").exists()
    ):
        validacion.conclusion = "Insatisfactoria"
    else:
        validacion.conclusion = "Satisfactoria"

    validacion.save()


@login_required(login_url="login_user")
def control_by_id(request, control_id):
    control = Control.objects.get(pk=control_id)
    return render(
        request,
        "control/control_by_id.html",
        {
            "control": control,
        },
    )


@login_required(login_url="login_user")
def add_encabezado_control(request, control_id):
    control = Control.objects.get(pk=control_id)
    encabezado = validate_existing_encabezado(control)
    submitted = False

    try:
        encabezado = control.encabezado
    except Encabezado.DoesNotExist:
        encabezado = None

    if request.method == "POST":
        if encabezado:
            form = EncabezadoControlForm(request.POST, instance=encabezado)
        else:
            form = EncabezadoControlForm(request.POST)
        if form.is_valid():
            encabezado = form.save(commit=False)
            encabezado.control = control
            estado = encabezado.estado
            if estado == "Terminado":
                if validate_estado_encabezado(control_id):
                    encabezado.save()
                    messages.success(
                        request,
                        ("Encabezado guardado con éxito."),
                    )
                    return HttpResponseRedirect("/control")
                else:
                    messages.success(
                        request,
                        (
                            "No se puede marcar como terminado un control sin evaluar el diseño."
                        ),
                    )
                    return render(
                        request,
                        "control/add_validacion_diseño.html",
                        {
                            "form": form,
                            "control": control,
                        },
                    )
        encabezado.save()
        messages.success(request, "Encabezado guardado con éxito.")
        return HttpResponseRedirect("/control")
    else:
        form = (
            EncabezadoControlForm(instance=encabezado)
            if encabezado
            else EncabezadoControlForm()
        )
        if "submitted" in request.GET:
            submitted = True
    return render(
        request,
        "control/add_encabezado_control.html",
        {"form": form, "submitted": submitted, "control": control},
    )


def validate_estado_encabezado(control_id):
    try:
        control = Control.objects.get(pk=control_id)
    except Control.DoesNotExist:
        raise Http404("Control no encontrado")

    validacion = ValidacionDiseño.objects.filter(control=control).first()
    if validacion:
        return True
    return False


def validate_existing_encabezado(control):
    try:
        return control.encabezado
    except Encabezado.DoesNotExist:
        return None
