from django.shortcuts import render, redirect, get_object_or_404
from .models import PublicacionPerroPerdido
from apps.users.models import CustomUser
from .forms import RegistrarPerroPerdido, ContactarNoRegistrado
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from pathlib import Path

import os
BASE_DIR = Path(__file__).resolve().parent.parent.parent


def ver_perdidos(request):
    if request.user.is_authenticated:
        publicaciones = PublicacionPerroPerdido.objects.exclude(
            usuario=request.user)
    else:
        publicaciones = PublicacionPerroPerdido.objects.all()
    paginator = Paginator(publicaciones, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    mostrar = publicaciones.count() > 0 and paginator.num_pages > 1
    return render(request, 'ver_perdidos.html', {'page_obj': page_obj, 'mostrar': mostrar})


@never_cache
@login_required
def ver_mis_perdidos(request):
    usuario = request.user
    publicaciones = PublicacionPerroPerdido.objects.filter(usuario=usuario)
    publicaciones_ordenadas = publicaciones.order_by('encontrado')
    paginator = Paginator(publicaciones_ordenadas, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    mostrar = publicaciones.count() > 0 and paginator.num_pages > 1
    return render(request, 'mis_perdidos.html', {'page_obj': page_obj, 'mostrar': mostrar})


@login_required
def cargar_perro_perdido(request):
    if request.method == 'POST':
        form = RegistrarPerroPerdido(request.POST, request.FILES)
        if form.is_valid():
            publicaciones = PublicacionPerroPerdido.objects.filter(
                usuario=request.user)
            publicacion = form.save(commit=False)
            publicacion.usuario = request.user
            if publicaciones.filter(nombre=publicacion.nombre).exists():
                messages.error(
                    request, "Ya has publicado un perro perdido con ese nombre.")
                return redirect('perdidos:cargar_perro_perdido')
            else:
                publicacion.save()
                messages.success(
                    request, "Se ha cargado el perro exitosamente.")
                return redirect('perdidos:ver_mis_perdidos')
    else:
        RegistrarPerroPerdido()
    return render(request, 'nuevo_perdido.html', {'registro_perdido': RegistrarPerroPerdido()})


def contactar_dueño_formulario(request, id_dueño, publicacion_id):
    if request.method == 'POST':
        form = ContactarNoRegistrado(request.POST)
        if form.is_valid():
            publicacion = get_object_or_404(
                PublicacionPerroPerdido, id=publicacion_id)
            dueño = get_object_or_404(CustomUser, id=id_dueño)
            email_contactante = request.POST['email']
            nombre = request.POST['nombre']
            apellido = request.POST['apellido']
            telefono = str(request.POST['telefono'])
            asunto = 'OhMyDog - Contacto de ' + nombre + \
                ' ' + apellido + ' - interesado en su publicación de ' + publicacion.titulo + '.'
            mensaje = 'El usuario ' + nombre + ' ' + apellido + ' con email ' + email_contactante + ' y telefono ' + \
                telefono + ' desea contactarse con usted por el perro que publicó en OhMyDog.'
            send_mail(
                asunto,
                mensaje,
                email_contactante,
                [dueño.email],
                fail_silently=False,
            )
            if publicacion.mails_contactados is None:
                publicacion.mails_contactados = {}
            publicacion.mails_contactados[email_contactante] = True
            publicacion.save()
            messages.success(
                request, "Se ha enviado su información de contacto exitosamente.")
            return redirect('perdidos:ver_perdidos')
    else:
        form = ContactarNoRegistrado()
    return render(request, os.path.join(BASE_DIR, 'apps', 'perdidos', 'templates', 'contactar_dueño_formulario.html'), {'form': form})


@login_required
def contactar_dueño(request, id_dueño, publicacion_id):
    if request.method == 'POST':
        publicacion = get_object_or_404(
            PublicacionPerroPerdido, id=publicacion_id)
        contactante = get_object_or_404(CustomUser, id=request.user.id)
        dueño = get_object_or_404(CustomUser, id=id_dueño)
        email_contactante = contactante.email
        nombre = contactante.nombre
        apellido = contactante.apellido
        telefono = str(contactante.telefono)
        asunto = 'OhMyDog - Contacto de ' + nombre + \
            ' ' + apellido + ' - se quiere comunicar con usted por la publicación ' + \
            publicacion.titulo + '.'
        mensaje = 'El usuario ' + nombre + ' ' + apellido + ' con email ' + email_contactante + ' y telefono ' + \
            telefono + ' desea contactarse con usted por la publicación que realizo en OhMyDog.'
        send_mail(
            asunto,
            mensaje,
            email_contactante,
            [dueño.email],
            fail_silently=False,
        )
        if publicacion.mails_contactados is None:
            publicacion.mails_contactados = {}
        publicacion.mails_contactados[email_contactante] = True
        publicacion.save()
        messages.success(
            request, "Se ha enviado su información de contacto exitosamente.")
        return redirect('perdidos:ver_perdidos')


@login_required
def borrar_perdido(request, publicacion_id):
    publicacion = PublicacionPerroPerdido.objects.get(id=publicacion_id)
    publicacion.delete()
    messages.success(
        request, "Se ha borrado la publicación exitosamente.")
    return redirect('perdidos:ver_mis_perdidos')


@login_required
def marcar_encontrado(request, publicacion_id):
    publicacion = PublicacionPerroPerdido.objects.get(id=publicacion_id)
    publicacion.encontrado = True
    publicacion.save()
    return redirect('perdidos:ver_mis_perdidos')


@login_required
def desmarcar_encontrado(request, publicacion_id):
    publicacion = PublicacionPerroPerdido.objects.get(id=publicacion_id)
    publicacion.encontrado = False
    publicacion.save()
    return redirect('perdidos:ver_mis_perdidos')
