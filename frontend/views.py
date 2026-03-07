from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import FormularioForm
from example.models import Formulario

# login screen

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # redirect based on role
            if user.is_staff or user.is_superuser:
                return redirect('home_admin')
            else:
                return redirect('cadastrar_formulario')
    else:
        form = AuthenticationForm()
    return render(request, 'frontend/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


def home_admin(request):
    if not request.user.is_authenticated or not (request.user.is_staff or request.user.is_superuser):
        return redirect('login')
    formularios = Formulario.objects.all().order_by('-created_at')
    return render(request, 'frontend/home_admin.html', {'formularios': formularios})


def cadastrar_formulario(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        form = FormularioForm(request.POST)
        if form.is_valid():
            formulario = form.save(commit=False)
            formulario.user = request.user
            formulario.save()
            return redirect('cadastrar_formulario')
    else:
        form = FormularioForm()
    return render(request, 'frontend/cadastrar_formulario.html', {'form': form})