from django.db import models
from apps.users.models import CustomUser
from apps.mascotas.models import Perro


class Turno (models.Model):
    TIME_CHOICES = (
        ('M', 'Mañana',),
        ('T', 'Tarde',),
    )
    Fecha =  models.DateField(auto_now=False, auto_now_add=False)
    Franja_Horaria  = models.TextField(
        max_length=1,
        choices=TIME_CHOICES,
    )
    Pendiente = models.BooleanField(default=False)
    Descripcion = models.TextField()
    Motivo = models.TextField()
    id_usuario = models.ForeignKey( 
        CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    id_perro = models.ForeignKey(
        Perro, on_delete=models.CASCADE, null=True, blank=True)
    
    # agregar demo3
    MOTIVOS = (
        ('Castrar', 'Castrar'),
        ('Vacunar', 'Vacunar'),
        ('Desparasitar', 'Desparasitar'),
        ('Consulta', 'Consulta')
    )
    MotivosConsulta = models.TextField(
        max_length=15,
        choices=MOTIVOS
    )
    # agregar demo3