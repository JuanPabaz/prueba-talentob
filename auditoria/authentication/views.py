from datetime import date
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
# Create your views here.

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        ano = request.POST['ano']
        testing = request.POST['testing']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            request.session['ano'] = ano
            request.session['testing'] = testing
            request.session['user_id'] = user.id
            login(request,user)
            return redirect(reverse('control_list'))
        else:
            messages.success(request,("Credenciales incorrectas"))
            return redirect('login_user')
    else:
        current_year = date.today().year 
        years = list(range(2022, current_year + 1))
        return render(request, 'authenticate/login.html',{'years': years})

def logout_user(request):
    logout(request)
    messages.success(request,("Cierre de sesion exitoso"))
    return redirect('login_user')

