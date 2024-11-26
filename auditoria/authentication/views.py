from datetime import date
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
# Create your views here.

def login_user(request):
    """
    Gestiona el proceso de inicio de sesión de un usuario, autentica las credenciales y establece sesiones para el año y ciclo.

    Args:
        request (HttpRequest): La solicitud HTTP.

    Returns:
        HttpResponse: Redirige a la vista `control_list` si el inicio de sesión es exitoso, o vuelve a la vista de login con un mensaje de error.
    """
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        ano = request.POST['ano']
        testing = request.POST['testing']
        # Se autentica el usuario
        user = authenticate(request,username=username,password=password)
        if user is not None:
            # Se guardan los campos enviados en el formulario de inicio de sesion en la sesion del aplicativo
            request.session['ano'] = ano
            request.session['testing'] = testing
            request.session['user_id'] = user.id
            login(request,user)
            # Se redirecciona a la pagina principal, la lista de controles del auditor
            return redirect(reverse('control_list'))
        else:
            messages.success(request,("Credenciales incorrectas"))
            return redirect('login_user')
    else:
        # Se crea la variable para mostrar los años desde el 2022 hasta el año actual
        current_year = date.today().year 
        years = list(range(2022, current_year + 1))
        return render(request, 'authenticate/login.html',{'years': years})

def logout_user(request):
    """
    Gestiona el cierre de sesión del usuario, eliminando las sesiones y redirigiendo a la vista de login.

    Args:
        request (HttpRequest): La solicitud HTTP.

    Returns:
        HttpResponse: Redirige a la vista `login_user` con un mensaje de éxito.
    """
    logout(request)
    messages.success(request,("Cierre de sesion exitoso"))
    return redirect('login_user')

