from django.shortcuts import render, redirect, get_object_or_404
from .models import PublicacionPerroEncontrado
from apps.users.models import CustomUser
from .forms import RegistrarPerroEncontrado, ContactarNoRegistrado
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from pathlib import Path

import os
BASE_DIR = Path(__file__).resolve().parent.parent.parent


def ver_encontrados(request):
    if request.user.is_authenticated:
        publicaciones = PublicacionPerroEncontrado.objects.exclude(
            usuario=request.user)
    else:
        publicaciones = PublicacionPerroEncontrado.objects.all()
    paginator = Paginator(publicaciones, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    mostrar = publicaciones.count() > 0 and paginator.num_pages > 1
    return render(request, 'ver_encontrados.html', {'page_obj': page_obj, 'mostrar': mostrar})


@never_cache
@login_required
def ver_mis_encontrados(request):
    usuario = request.user
    publicaciones = PublicacionPerroEncontrado.objects.filter(usuario=usuario)
    publicaciones_ordenadas = publicaciones.order_by('ubicado')
    paginator = Paginator(publicaciones_ordenadas, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    mostrar = publicaciones.count() > 0 and paginator.num_pages > 1
    return render(request, 'mis_encontrados.html', {'page_obj': page_obj, 'mostrar': mostrar})


@login_required
def cargar_perro_encontrado(request):
    if request.method == 'POST':
        form = RegistrarPerroEncontrado(request.POST, request.FILES)
        if form.is_valid():
            publicacion = form.save(commit=False)
            publicacion.usuario = request.user
            publicacion.save()
            messages.success(
                request, "Se ha cargado el perro exitosamente.")
            return redirect('encontrados:ver_mis_encontrados')
    else:
        form = RegistrarPerroEncontrado()
    return render(request, 'nuevo_encontrado.html', {'form': form})


def contactar_dueño_formulario(request, id_dueño, publicacion_id):
    if request.method == 'POST':
        form = ContactarNoRegistrado(request.POST)
        if form.is_valid():
            publicacion = get_object_or_404(
                PublicacionPerroEncontrado, id=publicacion_id)
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
            return redirect('encontrados:ver_encontrados')
    else:
        form = ContactarNoRegistrado()
    return render(request, os.path.join(BASE_DIR, 'apps', 'encontrados', 'templates', 'contactar_dueño_formulario.html'), {'form': form})


@login_required
def contactar_dueño(request, id, publicacion_id):
    if request.method == 'POST':
        publicacion = get_object_or_404(
            PublicacionPerroEncontrado, id=publicacion_id)
        contactante = get_object_or_404(CustomUser, id=request.user.id)
        dueño = get_object_or_404(CustomUser, id=id)
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
        return redirect('encontrados:ver_mis_encontrados')


@login_required
def borrar_encontrado(request, publicacion_id):
    publicacion = get_object_or_404(
        PublicacionPerroEncontrado, id=publicacion_id)
    publicacion.delete()
    messages.success(
        request, "Se ha borrado la publicación exitosamente")
    return redirect('encontrados:ver_mis_encontrados')


@login_required
def marcar_ubicado(request, publicacion_id):
    publicacion = PublicacionPerroEncontrado.objects.get(id=publicacion_id)
    publicacion.ubicado = True
    publicacion.save()
    return redirect('encontrados:ver_mis_encontrados')


@login_required
def desmarcar_ubicado(request, publicacion_id):
    publicacion = PublicacionPerroEncontrado.objects.get(id=publicacion_id)
    publicacion.ubicado = False
    publicacion.save()
    return redirect('encontrados:ver_mis_encontrados')
