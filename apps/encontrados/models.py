from django.db import models
from apps.users.models import CustomUser
from django.utils.translation import gettext_lazy as _


class PublicacionPerroEncontrado(models.Model):

    tamaño_choices = (('Chico', 'Chico'), ('Mediano', 'Mediano'), ('Grande', 'Grande'))
    edad_choices = (('Cachorro', 'Cachorro'), ('Joven', 'Joven'), ('Adulto', 'Adulto'))
    sexo_choices = (('Macho', 'Macho'), ('Hembra', 'Hembra'))
    titulo = models.CharField(max_length=100)
    zona = models.CharField(max_length=200)
    descripcion = models.TextField()
    ubicado = models.BooleanField(default=False)
    tamaño = models.CharField(max_length=100)
    rango_edad = models.CharField(max_length=30, choices=edad_choices)
    raza = models.CharField(max_length=100, blank=True)
    color = models.CharField(max_length=100, blank=True)
    sexo = models.CharField(max_length=20, blank=True)
    imagen = models.ImageField(upload_to='encontrados', blank=True)
    mails_contactados = models.JSONField(
        _("mails_contactados"), default=dict)
    usuario = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.Titulo
