from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from .models import Perro, HistoriaClinica, LibretaVacunas
from apps.users.models import CustomUser
from apps.turnos.models import Turno
from django.core.paginator import Paginator
from .forms import *
from django.contrib import messages
from datetime import datetime, date, timedelta, time
from django.views.decorators.cache import never_cache


def ver_mis_perros(request):
    usuario = get_object_or_404(CustomUser, id=request.user.id)
    perros = Perro.objects.filter(id_usuario_id=request.user.id)
    context = {'usuario': usuario, 'perros': perros}
    return render(request, 'mis_perros.html', context)


def ver_perros(request, id):
    usuario = get_object_or_404(CustomUser, id=id)
    perros = Perro.objects.filter(id_usuario_id=id)
    context = {'usuario': usuario, 'perros': perros}
    return render(request, 'ver_perros.html', context)


@never_cache
def historia_clinica(request, id):
    perro = get_object_or_404(Perro, id=id)
    registros = HistoriaClinica.objects.filter(perro_id=id)
    paginator = Paginator(registros, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    mostrar = registros.count() > 0 and paginator.num_pages > 1
    context = {'perro': perro, 'page_obj': page_obj, 'mostrar': mostrar}
    return render(request, 'historia_clinica.html', context)


@never_cache
def vacunas(request, id):
    perro = get_object_or_404(Perro, id=id)
    registros = LibretaVacunas.objects.filter(perro_id=id)
    paginator = Paginator(registros, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    mostrar = registros.count() > 0 and paginator.num_pages > 1
    context = {'perro': perro, 'page_obj': page_obj, 'mostrar': mostrar}
    return render(request, 'vacunas.html', context)


def registrar_mascota(request, id):
    if request.method == 'POST':
        form = RegistrarMascotaForm(request.POST)
        if form.is_valid():
            if Perro.objects.filter(id_usuario_id=id, nombre=form.cleaned_data['nombre']).exists():
                messages.error(
                    request, "Ya tienes una mascota registrada con ese nombre.")
            else:
                duenio = get_object_or_404(CustomUser, id=id)
                mascota = form.save(commit=False)
                mascota.id_usuario = duenio
                mascota.save()
                messages.success(
                    request, "Se ha registrado la mascota exitosamente.")
                return redirect('mascotas:ver_perros', id=id)
    else:
        form = RegistrarMascotaForm()
    return render(request, 'registrar_mascota.html', {'form': form})


def agregar_historia_clinica (request, id):
    if request.method == 'POST':
        form = RegistrarHistoriaForm(request.POST)
        if form.is_valid():
            perro = get_object_or_404(Perro, id=id)
            historiaclinica = form.save(commit=False)
            historiaclinica.perro = perro
            historiaclinica.save()
            messages.success(
                request, "La atención fue registrado exitosamente.")
            return redirect('mascotas:historia_clinica', id=id)
    else:
        form = RegistrarHistoriaForm()
    return render(request, 'agregar_historia_clinica.html', { 'form' : form })


def registrar_vacuna (request, id):

    fecha_actual = datetime.now()

    if request.method == 'POST':
        form = RegistrarVacunaForm(request.POST)
        if form.is_valid():
            vacuna = form.save(commit=False)
            if vacuna.numero_dosis <= 0 :
                messages.error( request, "El numero de dosis debe ser mayor a 0")
                return redirect('mascotas:registrar_vacuna', id=id)

            perro = get_object_or_404(Perro, id=id)
            vacuna.perro = perro

            edad_en_meses= (fecha_actual.year - perro.fecha_nacimiento.year) * 12 + fecha_actual.month - perro.fecha_nacimiento.month

            if vacuna.tipo == 'A': 

                if edad_en_meses < 4:
                    messages.error( request, "El perro debe tener al menos 4 meses para que se le pueda aplicar la vacuna antirrabica")
                    return redirect('mascotas:registrar_vacuna', id=id)
                else:
                    #generar solicitud de vacuna antirabica
                    dueño = get_object_or_404(CustomUser, email=perro.id_usuario)
                    turno = Turno()
                    turno.Fecha = vacuna.fecha + timedelta(days=365)
                    turno.id_usuario = dueño
                    turno.Franja_Horaria = 'M'
                    turno.Descripcion = "Aplicar la siguiente dosis de la vacuna antirrabica: " + vacuna.marca 

                    # si el dia es domingo, muevo la solicitud al lunes
                    dia_semana = turno.Fecha.weekday()
                    if dia_semana == 6:
                        turno.Fecha = turno.Fecha + timedelta(days=1)
                    vacuna.save()
                    turno.save()
                    print('generar solicitud de vacuna antirabica')
            else:
                if edad_en_meses < 2:
                    messages.error( request, "El perro debe tener al menos 2 meses para que se le pueda aplicar la vacuna del moquillo")
                    return redirect('mascotas:registrar_vacuna', id=id)
                
                else:
                    if edad_en_meses > 2 and edad_en_meses < 4:
                        #generar solicitud de vacuna moquillo
                        dueño = get_object_or_404(CustomUser, email=perro.id_usuario)
                        turno = Turno()
                        turno.Fecha = vacuna.fecha + timedelta(days=21)
                        turno.id_usuario = dueño
                        turno.Franja_Horaria = 'M'
                        turno.Descripcion = "Aplicar la siguiente dosis de la vacuna moquillo: " + vacuna.marca 

                        # si el dia es domingo, muevo la solicitud al lunes   
                        dia_semana = turno.Fecha.weekday()
                        if dia_semana == 6:
                            turno.Fecha = turno.Fecha + timedelta(days=1)
                        vacuna.save()
                        turno.save()
                        print('Generar solicitud de vacuna moquillo')
                    else:
                        #generar solicitud de vacuna moquillo
                        dueño = get_object_or_404(CustomUser, email=perro.id_usuario)
                        turno = Turno()
                        turno.Fecha = vacuna.fecha + timedelta(days=365)
                        turno.id_usuario = dueño
                        turno.Franja_Horaria = 'M'
                        turno.Descripcion = "Aplicar la siguiente dosis de la vacuna moquillo: " + vacuna.marca 

                        # si el dia es domingo, muevo la solicitud al lunes   
                        dia_semana = turno.Fecha.weekday()
                        if dia_semana == 6:
                            turno.Fecha = turno.Fecha + timedelta(days=1)
                        vacuna.save()
                        turno.save()
                        print('Generar solicitud de vacuna moquillo')
            messages.success(
                request, "la vacuna fue registrada exitosamente.")
            return redirect('mascotas:vacunas', id=id)
    else:
        form = RegistrarVacunaForm()
    return render(request, 'registrar_vacuna.html', { 'form' : form })


def registrar_castracion (request, id_perro):
    if request.method == 'POST':
        form = RegistarCastracionForm(request.POST)
        diagnostico = forms.CharField(required=False)
        if form.is_valid():
            diagnostico="Castración"
            perro = get_object_or_404(Perro, id=id_perro)
            perro.castrado = True
            historia_clinica = form.save(commit=False)
            historia_clinica.perro = perro
            historia_clinica.diagnostico = diagnostico
            historia_clinica.save()
            perro.save()
            messages.success(
                request, "La castracion fue registrada con exito")
            return redirect('mascotas:historia_clinica', id=id_perro)
    else:
        form = RegistarCastracionForm()
    return render(request, 'registrar_castracion.html', {'form' : form})


def borrar_vacuna(request, id_perro, id_vacuna):
    vacuna = get_object_or_404(LibretaVacunas, id=id_vacuna)
    vacuna.delete()
    messages.success(request, "La vacuna fue borrada con exito")
    return redirect('mascotas:vacunas', id=id_perro)


def borrar_historia (request, id_perro, id_historia):
    histoira = get_object_or_404(HistoriaClinica, id=id_historia)
    histoira.delete()
    messages.success(
        request, "La historia fue borrada con exito")
    return redirect('mascotas:historia_clinica', id=id_perro)