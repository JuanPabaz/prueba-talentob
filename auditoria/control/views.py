from django.shortcuts import get_object_or_404, render
from .models import Control, Auditor, Encabezado, Pregunta, Respuesta, ValidacionDiseño
from .forms import EncabezadoControlForm, ValidacionDiseñoForm
from django.http import Http404, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required(login_url="login_user")
def all_controls(request):
    """
    Obtiene todos los controles asignados a un auditor según el ciclo y año especificados.

    Args:
        request (HttpRequest): La solicitud HTTP.

    Returns:
        HttpResponse: Renderiza la vista `control_list.html` con los datos de los controles filtrados.
    """
    
    # Se obtienen los datos guardados en la sesion cuando se inició sesion
    ano = request.session.get("ano", None)
    testing = request.session.get("testing", None)
    usuario_id = request.session.get("user_id", None)
    auditor = get_object_or_404(Auditor, usuario_id=usuario_id)
    control_list = Control.objects.filter(auditor=auditor, año=ano, ciclo=testing)

    data = []
    # Se itera sobre la lista de controles para obtener sus encabezado y validacion
    for control in control_list:
        encabezado = getattr(control, "encabezado", None)
        validacion = getattr(control, "validacion", None)

        # Se obtienen los datos necesarios
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
    """
    Gestiona la validación del diseño de un control, incluyendo preguntas, respuestas y su conclusión.

    Args:
        request (HttpRequest): La solicitud HTTP.
        control_id (int): El ID del control a validar.

    Returns:
        HttpResponse: Renderiza la vista `add_validacion_diseño.html` o redirige a la lista de controles tras guardar.
    """
    # Se obtiene el control para asi mostrar los datos en la vista
    control = Control.objects.get(pk=control_id)
    # Se obtiene la lista de todas las preguntas para asi responderlas
    preguntas_list = Pregunta.objects.all()
    submitted = False
    # Se valida si ya existe una validacion para ese control
    validacion = validate_existing_validacion_diseño(control)
    # Se valida si la request es POST para saber si esta enviando el formulario o solo se esta consultando
    if request.method == "POST":
        # Si ya existe una validacion se muestra la vista con los datos ya guardados de la validacion
        if validacion:
            form = ValidacionDiseñoForm(request.POST, instance=validacion)
        else:
            form = ValidacionDiseñoForm(request.POST)
        if form.is_valid():
            validacion = form.save(commit=False)
            validacion.control = control
            # Se valida si se respondieron todas las respuestas o no para guardar la conclusion de la validacion
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

            # Se guarda la validacion y las respuestas a las preguntas
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
    """
    Verifica si existe una validación asociada a un control.

    Args:
        control (Control): El objeto de tipo Control.

    Returns:
        ValidacionDiseño: El objeto de validación asociado, o None si no existe.
    """
    try:
        return control.validacion
    except ValidacionDiseño.DoesNotExist:
        return None


def save_respuestas(preguntas_list, request, validacion):
    """
    Guarda las respuestas asociadas a una validación de diseño.

    Args:
        preguntas_list (QuerySet): Lista de preguntas.
        request (HttpRequest): La solicitud HTTP.
        validacion (ValidacionDiseño): El objeto de validación asociado.
    """
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
    """
    Valida si todas las respuestas han sido completadas para un conjunto de preguntas.

    Args:
        preguntas_list (QuerySet): Lista de preguntas.
        request (HttpRequest): La solicitud HTTP.

    Returns:
        None: Si ninguna respuesta ha sido completada.
        bool: True si todas están completas, False si faltan respuestas.
    """
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
    """
    Asigna una conclusión a una validación en función de las respuestas dadas.

    Args:
        validacion (ValidacionDiseño): El objeto de validación a calificar.
    """
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
    """
    Muestra los detalles de un control específico.

    Args:
        request (HttpRequest): La solicitud HTTP.
        control_id (int): El ID del control a consultar.

    Returns:
        HttpResponse: Renderiza la vista `control_by_id.html` con los detalles del control.
    """
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
    """
    Gestiona el encabezado de un control, permitiendo su creación o actualización.

    Args:
        request (HttpRequest): La solicitud HTTP.
        control_id (int): El ID del control asociado.

    Returns:
        HttpResponse: Renderiza la vista `add_encabezado_control.html` o redirige a la lista de controles tras guardar.
    """
    # Se obtiene el control para mostrar sus detalles
    control = Control.objects.get(pk=control_id)
    # Se valida si ya existe un encabezado para ese control
    encabezado = validate_existing_encabezado(control)
    submitted = False

    try:
        encabezado = control.encabezado
    except Encabezado.DoesNotExist:
        encabezado = None

    # Se valida si la request es POST para saber si esta enviando el formulario o solo se esta consultando
    if request.method == "POST":
        # Si ya existe un encabezado se retorna los campos con los valores ya guardados de ese encabezado
        if encabezado:
            form = EncabezadoControlForm(request.POST, instance=encabezado)
        else:
            form = EncabezadoControlForm(request.POST)
        if form.is_valid():
            encabezado = form.save(commit=False)
            encabezado.control = control
            estado = encabezado.estado
            # Se verifica el estado del encabezado
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
        # Se guarda el encabezado
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
    """
    Valida si un control puede marcarse como terminado verificando la existencia de su validación.

    Args:
        control_id (int): El ID del control a validar.

    Returns:
        bool: True si la validación existe, False en caso contrario.

    Raises:
        Http404: Si el control no existe.
    """
    try:
        control = Control.objects.get(pk=control_id)
    except Control.DoesNotExist:
        raise Http404("Control no encontrado")

    validacion = ValidacionDiseño.objects.filter(control=control).first()
    if validacion:
        return True
    return False


def validate_existing_encabezado(control):
    """
    Verifica si existe un encabezado asociado a un control.

    Args:
        control (Control): El objeto de tipo Control.

    Returns:
        Encabezado: El objeto de encabezado asociado, o None si no existe.
    """
    try:
        return control.encabezado
    except Encabezado.DoesNotExist:
        return None
