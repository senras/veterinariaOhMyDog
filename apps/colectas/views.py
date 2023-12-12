from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Colecta, Donacion, EmailDonacionHardcode
from apps.users.models import CustomUser
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from .forms import NuevaColecta, NuevaDonacion
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import mercadopago

# Acces token de vendedor
ACCESS_TOKEN = "APP_USR-1703013437091741-061814-51e2b39866dbc7b6f8f08539a829b083-1401765295"
sdk = mercadopago.SDK(ACCESS_TOKEN)


def mostrar_colectas(request):
    colectas = Colecta.objects.all().order_by('fecha_limite')
    for colecta in colectas:
        numero = round((colecta.monto_recaudado / colecta.monto_meta) * 100, 2)
        colecta.porcentaje = str(numero)
        colecta.save()
        colecta.numero = numero
    paginator = Paginator(colectas, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    mostrar = colectas.count() > 0 and paginator.num_pages > 1
    return render(request, 'mostrar_colectas.html', {'page_obj': page_obj, 'mostrar': mostrar})


@login_required
def nueva_colecta(request):
    if request.method == 'POST':
        form = NuevaColecta(request.POST)
        if form.is_valid():
            monto_meta = form.cleaned_data['monto_meta']
            if (monto_meta < 0 ):
                messages.error(
                    request, "el monto debe ser postivo")
                return redirect('colectas:nueva_colecta')

            titulo = form.cleaned_data['titulo']
            descripcion = form.cleaned_data['descripcion']
            fecha_limite = form.cleaned_data['fecha_limite']

            Colecta.objects.create(
                titulo=titulo,
                descripcion=descripcion,
                monto_meta=monto_meta,
                fecha_limite=fecha_limite
            )

            messages.success(
                request, "Se ha creado la colecta exitosamente")

            return redirect('colectas:mostrar_colectas')
    else:
        form = NuevaColecta()

    return render(request, 'nueva_colecta.html', {'nueva_colecta': form})


@login_required
def borrar_colecta(request, colecta_id):
    colecta = Colecta.objects.get(id=colecta_id)
    colecta.delete()
    messages.success(request, "Se ha borrado la colecta exitosamente.")
    return redirect('colectas:mostrar_colectas')


@login_required
def marcar_concluida(request, colecta_id):
    colecta = Colecta.objects.get(id=colecta_id)
    colecta.concluida = True
    colecta.save()
    messages.success(request, "Se ha concluido la colecta exitosamente.")
    return redirect('colectas:mostrar_colectas')


@login_required
def desmarcar_concluida(request, colecta_id):
    colecta = Colecta.objects.get(id=colecta_id)
    colecta.concluida = False
    colecta.save()
    messages.success(request, "La colecta está activa nuevamente.")
    return redirect('colectas:mostrar_colectas')


def pantalla_donacion(request, colecta_id):
    if request.method == 'POST':
        form = NuevaDonacion(request.POST)
        if form.is_valid():

            #validacion si no es usuario logueado para crear el wrapper
            if(not request.user.is_authenticated):
                wrrap = EmailDonacionHardcode()
                wrrap.email = request.POST.get('mail')
                unacolecta = get_object_or_404(Colecta, id=colecta_id)
                wrrap.colecta = unacolecta
                wrrap.save() 

            monto = request.POST.get('monto')
            return redirect('colectas:donar_colecta', colecta_id, monto)
    else:
        form = NuevaDonacion()
    return render(request, 'pantalla_donacion.html', {"colecta_id": colecta_id, 'form': form, })


def donar_colecta(request, colecta_id, monto):
    ml_link = "https://4485-186-143-134-179.ngrok-free.app"
    try:
        preference_data = {
            # cambiar las urls cada vez que se inicia ngrok, desde https hasta app
            "back_urls": {
                "success": ml_link+"/colectas/success",
                "failure": ml_link+"/colectas/failure",
                "pending": ml_link+"/colectas/pending",
            },
            "items": [
                {
                    "title": "Mi primer colecta",
                    "quantity": 1,
                    "unit_price": monto,
                    "id": colecta_id,
                    "currency_id": "ARS"
                }
            ],
            "description": "Donacion a colecta",
            "installments": 1,
        }
        preference_response = sdk.preference().create(preference_data)
        preference = preference_response["response"]
        # return JsonResponse(data={"body": preference}, status=201)
        mp_url = preference["init_point"]
        return redirect(mp_url)
    except Exception as e:
        return JsonResponse(data={"body": preference}, status=400)


def success(request):
    payment_id = request.GET.get('payment_id')
    payment = sdk.payment().get(payment_id)
    producto = payment["response"]["additional_info"]["items"][0]
    colecta = Colecta.objects.get(id=producto["id"])
    monto = float(producto["unit_price"])
    colecta.monto_recaudado += float(producto["unit_price"])
    colecta.save()

    if(not request.user.is_authenticated):
        emaildonacion = EmailDonacionHardcode.objects.latest('id')
        Donacion.objects.create(monto=monto, colecta=colecta, email=emaildonacion.email)
    else:
        user = get_object_or_404(CustomUser, id=request.user.id)
        Donacion.objects.create(monto=monto, colecta=colecta, donador_id=user.id)
    
    # donacion = Donacion.objects.create(
    #     monto=monto, colecta=colecta, usuario=mail)
    messages.success(
        request, "Gracias por colaborar con su donación ($"+str(monto)+")!")
    return redirect('colectas:mostrar_colectas')


def failure(request):
    messages.error(
        request, "No se pudo concretar la donación, por favor intente más tarde")
    return redirect('colectas:mostrar_colectas')


def pending(request):
    messages.warning("Su donación está pendiente de aprobación")
    return redirect('colectas:mostrar_colectas')


def notification(request):
    payment_id = request.GET.get('payment_id')
    payment = sdk.payment().get(payment_id)
    producto = payment["response"]["additional_info"]["items"][0]
    colecta = Colecta.objects.get(id=producto["id"])
    colecta.monto_recaudado += float(producto["unit_price"])
    colecta.save()


def mostrar_detalle_colecta(request, colecta_id):
    colecta = Colecta.objects.get(id=colecta_id)
    donaciones = Donacion.objects.filter(colecta=colecta_id)
    paginator = Paginator(donaciones, 20)
    page_number = request.GET.get('page')
    mostrar = donaciones.count() > 0 and paginator.num_pages > 1
    page_obj = paginator.get_page(page_number)
    context = {'colecta': colecta, 'mostrar': mostrar, 'page_obj': page_obj}
    return render(request, 'detalle_colecta.html', context)
