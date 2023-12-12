from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from .models import CustomUser


from pathlib import Path
import os
from .forms import CustomUserCreationForm, CustomUserChangeInfoForm, CustomUserChangePasswordForm, RecoverAccountForm

BASE_DIR = Path(__file__).resolve().parent.parent.parent


def index(request):
    return render(request, os.path.join(BASE_DIR, 'apps', 'users', 'templates', 'index.html'))


def crear_cliente(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        email = request.POST.get('email')
        if form.is_valid():
            if not CustomUser.objects.filter(email=email).exists():
                form.save()
                messages.success(
                    request, "Se ha creado el cliente exitosamente.")
                return redirect('users:mostrar_usuarios')
            else:
                messages.error(request, "El correo ingresado ya existe")
    else:
        form = CustomUserCreationForm()
    return render(request, os.path.join(BASE_DIR, 'apps', 'users', 'templates', 'crear_cliente.html'), {'form': form, })


def cambiar_info(request):
    if request.method == 'POST':
        user = get_object_or_404(CustomUser, id=request.user.id)
        form = CustomUserChangeInfoForm(request.POST, instance=request.user)
        email = request.POST.get('email')
        direccion = request.POST.get('direccion')
        telefono = int(request.POST.get('telefono') or 0)
        if form.is_valid():
            if direccion != "":
                user.direccion = direccion
            if telefono != 0:
                user.telefono = telefono
            if email != "":
                if not CustomUser.objects.filter(email=email).exists():
                    user.email = email
                else:
                    messages.error(request, "El correo ingresado ya existe")
            user.save()
            messages.success(
                request, "Se han guardado los cambios realizados exitosamente.")
            return redirect('users:mi_perfil')
    else:
        form = CustomUserChangeInfoForm(request.POST, instance=request.user)
    return render(request, os.path.join(BASE_DIR, 'apps', 'users', 'templates', 'cambiar_info.html'), {'form': form, 'user': request.user, })


def cambiar_contraseña(request):
    if request.method == 'POST':
        form = CustomUserChangePasswordForm(
            user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(
                request, ("Se cambio la contraseña exitosamente!"))
            return redirect('users:logout')
    else:
        form = CustomUserChangePasswordForm(user=request.user)
    return render(request, os.path.join(BASE_DIR, 'apps', 'users', 'templates', 'cambiar_contraseña.html'), {'form': form, 'user': request.user, })


def mi_perfil(request):
    return render(request, os.path.join(BASE_DIR, 'apps', 'users', 'templates', 'mi_perfil.html'), {'user': request.user, })


def recuperar_cuenta(request):
    if request.method == 'POST':
        form = RecoverAccountForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            if CustomUser.objects.filter(email=email).exists():
                # CustomUser.objects.update(password='12345678')
                subject = 'Recuperación de cuenta'
                message = 'Contraseña temporal: 12345678'
                from_email = 'ohmydog@gmail.com'
                send_mail(
                    subject,
                    message,
                    from_email,
                    [email],
                    fail_silently=False,
                )
                messages.success(
                    request, 'Se ha enviado un correo con la contraseña temporal')
                return redirect('users:login')
            else:
                messages.error(request, 'El correo ingresado no existe')
                return redirect('users:login')
    else:
        form = RecoverAccountForm()
    return render(request, os.path.join(BASE_DIR, 'apps', 'users', 'templates', 'recuperar_cuenta.html'), {'form': form})


def mostrar_usuarios(request):
    usuarios = CustomUser.objects.exclude(es_veterinario=True)
    paginator = Paginator(usuarios, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    mostrar = usuarios.count() > 0 and paginator.num_pages > 1
    context = {'page_obj': page_obj, 'mostrar': mostrar}
    return render(request, 'mostrar_usuarios.html', context)


def mostrar_perfil(request, id):
    usuario = get_object_or_404(CustomUser, id=id)
    context = {'usuario': usuario}
    return render(request, 'mostrar_perfil.html', context)
