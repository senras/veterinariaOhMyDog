from django.db import models
from apps.users.models import CustomUser
from django.utils import timezone


class Perro (models.Model):
    SEX_CHOICES = (
        ('H', 'Hembra',),
        ('M', 'Macho',),
    )
    tamaño_choices = (('Chico', 'Chico'), ('Mediano',
                      'Mediano'), ('Grande', 'Grande'))
    nombre = models.CharField(max_length=100)
    raza = models.CharField(max_length=100)
    color = models.CharField(max_length=100, )
    sexo = models.CharField(
        max_length=1,
        choices=SEX_CHOICES,
    )
    castrado = models.BooleanField()
    tamaño = models.CharField(max_length=8,
                              choices=tamaño_choices, default='Chico')
    fecha_nacimiento = models.DateField(
        auto_now=False, auto_now_add=False, default=timezone.now)
    id_usuario = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['nombre']


class LibretaVacunas(models.Model):

    def __str__(self):
        return self.Marca

    TYPE_CHOICES = (
        ('A', 'Antirrabica',),
        ('M', 'Moquillo',),
    )

    fecha = models.DateField(auto_now=False, auto_now_add=False)
    marca = models.CharField(max_length=100)
    tipo = models.CharField(
        max_length=1,
        choices=TYPE_CHOICES,
    )
    lote = models.CharField(max_length=100)
    numero_dosis = models.IntegerField()
    perro = models.OneToOneField(
        'Perro', on_delete=models.CASCADE, related_name='LibretaVacunas')

    class Meta:
        ordering = ['fecha']


class HistoriaClinica(models.Model):

    def __str__(self):
        return self.Fecha

    fecha = models.DateField(auto_now=False, auto_now_add=False)
    peso = models.TextField(default='')
    descripcion = models.TextField()
    diagnostico = models.TextField(default='')
    perro = models.OneToOneField(
        'Perro', on_delete=models.CASCADE, related_name='HistoriaClinica')

    class Meta:
        ordering = ['fecha']
