from django.core.mail import send_mail
from django.template.loader import render_to_string
from veterinaria_oh_my_dog import settings
from celery import shared_task
from django.shortcuts import get_object_or_404
from .models import Turno
from apps.users.models import CustomUser


@shared_task(bind=True)
def enviar_recordatorio(self, turno_id):
    turno = get_object_or_404(Turno, id=turno_id)
    usuario = get_object_or_404(CustomUser, email=turno.id_usuario)
    subject = f'Recordatorio: turno el dia {turno.Fecha.day}/{turno.Fecha.month}'
    message = render_to_string('recordatorio.html', {'turno': turno})
    from_email = 'ohmydog@gmail.com'
    to_mail = usuario.email
    send_mail(
        subject, 
        message, 
        from_email, 
        [to_mail],
        fail_silently=False,
        )
    return f"{message}"
