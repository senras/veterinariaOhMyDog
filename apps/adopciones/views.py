from django.shortcuts import render, redirect, get_object_or_404
from .models import PublicacionPerroAdopcion
from apps.users.models import CustomUser
from .forms import RegistrarPerroEnAdopcion, ContactarDueñoNoRegistrado
from django.core.mail import send_mail
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.contrib import messages


from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve().parent.parent.parent


def mostrar_publicaciones(request):
    if request.user.is_authenticated:
        publicaciones = PublicacionPerroAdopcion.objects.exclude(
            usuario=request.user)
    else:
        publicaciones = PublicacionPerroAdopcion.objects.all()
    paginator = Paginator(publicaciones, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    mostrar = publicaciones.count() > 0 and paginator.num_pages > 1
    return render(request, 'index_adopciones.html', {'page_obj': page_obj, 'mostrar': mostrar})


def cargar_perro_adopcion(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        zona = request.POST.get('zona')
        descripcion = request.POST.get('descripcion')
        raza = request.POST.get('raza')
        color = request.POST.get('color')
        sexo = request.POST.get('sexo')
        tamaño = request.POST.get('tamaño')
        rango_edad = request.POST.get('rango_edad')
        usuario = request.user
        PublicacionPerroAdopcion.objects.create(
            titulo=titulo,
            zona=zona,
            descripcion=descripcion,
            raza=raza,
            color=color,
            sexo=sexo,
            tamaño=tamaño,
            rango_edad=rango_edad,
            usuario=usuario
        )
        messages.success(
            request, "Se ha cargado el perro en adopción exitosamente.")

        return redirect('adopciones:mostrar_publicaciones')
    else:
        return render(request, 'nueva_publicacion.html', {'registro_adopcion': RegistrarPerroEnAdopcion()}) 


def contactar_dueño_formulario(request, id, titulo):
    if request.method == 'POST':
        form = ContactarDueñoNoRegistrado(request.POST)
        if form.is_valid():
            dueño = get_object_or_404(CustomUser, id=id)
            email_contactante = request.POST['email']
            nombre = request.POST['nombre']
            apellido = request.POST['apellido']
            telefono = str(request.POST['telefono'])
            asunto = 'OhMyDog - Contacto de ' + nombre + \
                ' ' + apellido + ' - interesado en su publicación de ' + titulo + '.'
            mensaje = 'El usuario ' + nombre + ' ' + apellido + ' con email ' + email_contactante + ' y telefono ' + \
                telefono + ' desea contactarse con usted por el perro que publicó en OhMyDog.'
            print(dueño.email)
            send_mail(
                asunto,
                mensaje,
                email_contactante,
                [dueño.email],
                fail_silently=False,
            )
            messages.success(
                request, "Se ha enviado su información de contacto exitosamente.")
            return redirect('adopciones:mostrar_publicaciones')
    else:
        form = ContactarDueñoNoRegistrado()
    return render(request, os.path.join(BASE_DIR, 'apps', 'adopciones', 'templates', 'contactar_dueño_formulario.html'), {'form': form})


def contactar_dueño(request, id, titulo, publicacion_id):
    if request.method == 'POST':
        print(request.user)
        contactante = get_object_or_404(CustomUser, id=request.user.id)
        dueño = get_object_or_404(CustomUser, id=id)
        email_contactante = contactante.email
        nombre = contactante.nombre
        apellido = contactante.apellido
        telefono = str(contactante.telefono)
        asunto = 'OhMyDog - Contacto de ' + nombre + \
            ' ' + apellido + ' - interesado en su publicación de ' + titulo + '.'
        mensaje = 'El usuario ' + nombre + ' ' + apellido + ' con email ' + email_contactante + ' y telefono ' + \
            telefono + ' desea contactarse con usted por el perro que publicó en OhMyDog.'
        print(dueño.email)
        send_mail(
            asunto,
            mensaje,
            email_contactante,
            [dueño.email],
            fail_silently=False,
        )
        if contactante.publicaciones_contactadas is None:
            contactante.publicaciones_contactadas = {}
        contactante.publicaciones_contactadas[publicacion_id] = True
        contactante.save()
        messages.success(
            request, "Se ha enviado su información de contacto exitosamente.")
        return redirect('adopciones:mostrar_publicaciones')


@never_cache
def mostrar_publicaciones_adopcion(request):
    usuario = request.user
    publicaciones = PublicacionPerroAdopcion.objects.filter(usuario=usuario)
    publicaciones_ordenadas = publicaciones.order_by('adoptado')
    paginator = Paginator(publicaciones_ordenadas, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'mis_publicaciones_adopcion.html', {'page_obj': page_obj})


def borrar_publicacion_adopcion(request, publicacion_id):
    publicacion = get_object_or_404(
        PublicacionPerroAdopcion, id=publicacion_id)
    publicacion.delete()
    messages.success(
        request, "Se ha borrado la publicación de adopción exitosamente.")

    return redirect('adopciones:mostrar_publicaciones_adopcion')


def marcar_adoptado(request, publicacion_id):
    publicacion = PublicacionPerroAdopcion.objects.get(id=publicacion_id)
    publicacion.adoptado = True
    publicacion.save()
    return redirect('adopciones:mostrar_publicaciones_adopcion')


def desmarcar_adoptado(request, publicacion_id):
    publicacion = PublicacionPerroAdopcion.objects.get(id=publicacion_id)
    publicacion.adoptado = False
    publicacion.save()
    return redirect('adopciones:mostrar_publicaciones_adopcion')

