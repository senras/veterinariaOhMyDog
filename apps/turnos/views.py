from .forms import RegistrarTurno
from django.shortcuts import render, get_object_or_404, redirect
from apps.users.models import CustomUser
from apps.mascotas.models import Perro
from .models import Turno
from django.contrib import messages
from django.core.paginator import Paginator
from datetime import datetime, date, timedelta, time
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


def turnos_main(request):
    usuario = get_object_or_404(CustomUser, id=request.user.id)
    return render(request, 'navegador.html',{
        'usuario' : usuario,
    })


def ver_turnos (request):
    if request.method == 'POST' :
        fecha_inicio = request.POST.get('fechaInicio')
        fecha_fin = request.POST.get('fechaFin')

        if not fecha_fin or not fecha_inicio:
            messages.error(request, "Debe ingresar ambas fechas.")
            return redirect('turnos:mostrar_turnos')
        if fecha_inicio > fecha_fin:
            messages.error(request, "La fecha inicial no puede ser posterior a la fecha final.")
            return redirect('turnos:mostrar_turnos')
        turnos = Turno.objects.filter(Fecha__range=[fecha_inicio, fecha_fin], Pendiente=True).filter(Motivo__exact='').order_by('Fecha')
        
        paginator = Paginator(turnos, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        mostrar = turnos.count() > 0 and paginator.num_pages > 1
        context = {'page_obj': page_obj, 'mostrar': mostrar}
        return render(request, 'mostrar_turnos.html', context)
        

    else :
        turnos = Turno.objects.exclude(Pendiente=False).filter(Motivo__exact='').order_by('Fecha')
        paginator = Paginator(turnos, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        mostrar = turnos.count() > 0 and paginator.num_pages > 1
        context = {'page_obj': page_obj, 'mostrar': mostrar}
    return render(request, 'mostrar_turnos.html', context)


def pedir_turno (request):
    if request.method == 'POST':
        form = RegistrarTurno(request.POST)
        if form.is_valid():
        
            turno = form.save(commit=False)

            #validar perro
            idperro = request.POST.get('idperro')

            if idperro != 'null' :
                perro = get_object_or_404(Perro, id=idperro)
                turno.id_perro = perro

            dueño = request.user

            turno.id_usuario = dueño

            dia_semana = turno.Fecha.weekday()
            franja_horaria = turno.Franja_Horaria
           
           # Verificar si la fecha es posterior a la fecha actual
            fecha_actual = date.today()

            if turno.Fecha <= fecha_actual:
                messages.error(request, "La fecha debe ser posterior a la fecha actual.")
                return redirect('turnos:solicitar_turno')
            
            if dia_semana == 5:  # Sábado
                if franja_horaria == 'T':
                    messages.error(request, "Los turnos del sábado solo pueden ser por la mañana.")
                    return redirect('turnos:solicitar_turno')
            elif dia_semana == 6: # domingo
                    messages.error(request, "No se puede solicitar turnos los domingos.")
                    return redirect('turnos:solicitar_turno')
            turno.save()
            messages.success(request, "Se ha registrado el turno exitosamente.")
            return redirect('turnos:mis_turnos')
    else:
        form = RegistrarTurno()
        dueño = request.user
        perros = Perro.objects.filter(id_usuario_id=dueño.id)
        context = {
            'form': form,
            'perros': perros,

        }    
        return render(request, 'solicitar_turno.html', context)

def ver_turnos_pendientes(request):
    if request.method == 'POST' :

        fecha_inicio = request.POST.get('fechaInicio')
        fecha_fin = request.POST.get('fechaFin')

        if not fecha_fin or not fecha_inicio:
            messages.error(request, "Debe ingresar ambas fechas.")
            return redirect('turnos:turnos_pendientes')
        if fecha_inicio > fecha_fin:
            messages.error(request, "La fecha inicial no puede ser posterior a la fecha final.")
            return redirect('turnos:turnos_pendientes')
        turnos = Turno.objects.filter(Fecha__range=[fecha_inicio, fecha_fin], Pendiente=False).order_by('Fecha')
        
        paginator = Paginator(turnos, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        mostrar = turnos.count() > 0 and paginator.num_pages > 1
        context = { 'page_obj': page_obj, 'mostrar': mostrar }
        return render(request, 'turnos_pendientes.html', context)
        

    else :
        turnos = Turno.objects.exclude(Pendiente=True).order_by('Fecha')
        paginator = Paginator(turnos, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        mostrar = turnos.count() > 0 and paginator.num_pages > 1
        context = {'page_obj': page_obj, 'mostrar': mostrar}
        return render(request, 'turnos_pendientes.html', context)


def tiempo_espera(horas, turno):
    fecha_actual = datetime.combine(date.today(), datetime.now().time())
    #parseo la fecha del turno para que pueda restarse utilizando timedelta
    fecha_turno = datetime(turno.Fecha.year, turno.Fecha.month, turno.Fecha.day, 0, 0, 0)
    fecha_diferencia = fecha_turno - timedelta(hours=horas)

    if fecha_diferencia < fecha_actual:
        return fecha_actual
    else:
        return fecha_diferencia


def tiempo_espera_minutos(minutos, turno):
    fecha_actual = datetime.combine(date.today(), datetime.now().time())
    #parseo la fecha del turno para que pueda restarse utilizando timedelta
    fecha_turno = datetime(turno.Fecha.year, turno.Fecha.month, turno.Fecha.day, 0, 0, 0)
    fecha_diferencia = fecha_turno - timedelta(minutes=minutos)

    if fecha_diferencia < fecha_actual:
        return fecha_actual
    else:
        return fecha_diferencia

 
def aceptar_turno(request, id):
    from .tasks import enviar_recordatorio

    turno = get_object_or_404(Turno, id=id)
    fecha_recordatorio = tiempo_espera(72, turno)
    # enviar_recordatorio.apply_async(args=[turno.id], eta=fecha_recordatorio)
    fecha_recordatorio = tiempo_espera(24, turno)
    # enviar_recordatorio.apply_async(args=[turno.id], eta=fecha_recordatorio)
    turno.Pendiente=True

    turno.save()

    messages.success(
        request, "El turno fue aceptado exitosamente.")

    return redirect('turnos:turnos_pendientes')


def rechazar_turno(request, id):

    campoMotivo = request.POST.get('motivoRechazo')

    if not campoMotivo:
            messages.error(request, "se debe ingresar un motivo")
            return redirect('turnos:turnos_pendientes')
    
    turno = get_object_or_404(Turno, id=id)
    print('esto contiene la variable campoMotivo')
    print(campoMotivo)
    subject = 'turno cancelado'
    message = f"El turno del dia {turno.Fecha} fue cancelado por {campoMotivo}, por favor solicite otro turno"
    from_email = 'ohmydog@gmail.com'
    usuario = get_object_or_404(CustomUser, email=turno.id_usuario)
    to_mail = usuario.email
    send_mail(
        subject, 
        message, 
        from_email, 
        [to_mail],
        fail_silently=False,
        )
    turno.Pendiente=True
    turno.Motivo=campoMotivo
    turno.save()
    messages.success(
        request, "El cliente fue notificado")
    return redirect('turnos:turnos_pendientes')

def mis_turnos(request):
    usuario = get_object_or_404(CustomUser, id=request.user.id)
    turnos = Turno.objects.filter(id_usuario_id=request.user.id).order_by('Fecha')
    context = {'usuario': usuario, 'turnos': turnos}
    return render(request, 'mis_turnos.html', context)