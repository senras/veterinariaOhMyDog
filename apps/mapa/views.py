from django.shortcuts import render, redirect, get_object_or_404
from .models import Paseador_cuidador
from apps.users.models import CustomUser
from django.core.mail import send_mail


from .forms import RegistrarPaseador_CuidadorForm, ContactarPaseadorCuidadorForm
from django.contrib import messages


def mostrar_mapa_veterinario(request):
    ubicaciones = list(Paseador_cuidador.objects.values())
    if request.method == 'POST':
        form = RegistrarPaseador_CuidadorForm(request.POST)
        if form.is_valid():
            paseador_cuidador = form.save(commit=False)
            paseador_cuidador.save()
            messages.success(
                request, "Se ha cargado exitosamente.")
            return redirect('mapa:mostrar_mapa_veterinario')
    else:
        form = RegistrarPaseador_CuidadorForm()
    return render(request, 'mapa-veterinario.html', {'form': form, 'ubicaciones': ubicaciones})


def mostrar_mapa_usuario(request):
    ubicaciones = list(Paseador_cuidador.objects.values())
    return render(request, 'mapa-usuario.html', {'ubicaciones': ubicaciones})


def registrar_paseador_cuidador(request):
    if request.method == 'POST':
        form = RegistrarPaseador_CuidadorForm(request.POST, auto_id=True)
        if form.is_valid():
            paseador_cuidador = form.save(commit=False)
            paseador_cuidador.save()
            messages.success(
                request, "Se ha cargado exitosamente.")
            return redirect('mapa:mostrar_mapa_veterinario')
    else:
        form = RegistrarPaseador_CuidadorForm()
    return render(request, 'registrar_paseador_cuidador.html', {'form': form})


def borrar_paseador_cuidador(request, id):
    paseador_cuidador = Paseador_cuidador.objects.get(id=id)
    paseador_cuidador.delete()
    messages.success(
        request, "Se ha eliminado exitosamente.")
    return redirect('mapa:mostrar_mapa_veterinario')


def marcar_disponible(request, id):
    paseador_cuidador = Paseador_cuidador.objects.get(id=id)
    paseador_cuidador.disponible = True
    paseador_cuidador.save()
    messages.success(
        request, "Se ha marcado como disponible.")
    return redirect('mapa:mostrar_mapa_veterinario')


def marcar_no_disponible(request, id):
    paseador_cuidador = Paseador_cuidador.objects.get(id=id)
    paseador_cuidador.disponible = False
    paseador_cuidador.save()
    messages.success(
        request, "Se ha marcado como no disponible.")
    return redirect('mapa:mostrar_mapa_veterinario')


def modificar_paseador_cuidador(request, id):
    paseador_cuidador = get_object_or_404(Paseador_cuidador, id=id)
    if request.method == 'GET':
        form = RegistrarPaseador_CuidadorForm(instance=paseador_cuidador)
    else:
        form = RegistrarPaseador_CuidadorForm(
            request.POST, instance=paseador_cuidador)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Se ha modificado exitosamente.")
            return redirect('mapa:mostrar_mapa_veterinario')
    return render(request, 'registrar_paseador_cuidador.html', {'form': form})


def contactar(request, id):
    paseador_cuidador = get_object_or_404(Paseador_cuidador, id=id)
    if request.user.is_authenticated:
        # Contactar usuario registrado
        contactante = get_object_or_404(CustomUser, id=request.user.id)
        email_contactante = contactante.email
        nombre = contactante.nombre
        apellido = contactante.apellido
        telefono = str(contactante.telefono)
        asunto = 'OhMyDog - Contacto de ' + nombre + \
            ' ' + apellido + ' - interesado por sus servicios'
        mensaje = 'El usuario ' + nombre + ' ' + apellido + ' con email ' + email_contactante + ' y teléfono ' + \
            telefono + ' desea contactarse con usted por sus servicios.'
        send_mail(
            asunto,
            mensaje,
            email_contactante,
            [paseador_cuidador.mail],
            fail_silently=False,
        )
        messages.success(
            request, "Se ha enviado su información de contacto exitosamente.")
        return redirect('mapa:mostrar_mapa_usuario')
    else:
        # Contactar usuario no registrado
        if request.method == 'POST':
            form = ContactarPaseadorCuidadorForm(request.POST)
            if form.is_valid():
                email_contactante = request.POST['email']
                nombre = request.POST['nombre']
                apellido = request.POST['apellido']
                telefono = str(request.POST['telefono'])
                asunto = 'OhMyDog - Contacto de ' + nombre + \
                    ' ' + apellido + ' - interesado por sus servicios'
                mensaje = 'El usuario ' + nombre + ' ' + apellido + ' con email ' + email_contactante + ' y telefono ' + \
                    telefono + ' desea contactarse con usted por sus servicios.'
                send_mail(
                    asunto,
                    mensaje,
                    email_contactante,
                    [paseador_cuidador.mail],
                    fail_silently=False,
                )
                messages.success(
                    request, "Se ha contactado exitosamente.")
                return redirect('mapa:mostrar_mapa_usuario')
        else:
            form = ContactarPaseadorCuidadorForm()
        return render(request, 'contactar.html', {'form': form})
