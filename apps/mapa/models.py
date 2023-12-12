from django.db import models


class Paseador_cuidador(models.Model):
    servicio_choices = (("Paseador", "Paseador"), ("Cuidador", "Cuidador"))
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    telefono = models.CharField(max_length=50)
    zona = models.CharField(max_length=50)
    mail = models.CharField(max_length=50)
    tipo_servicio = models.CharField(max_length=20, choices=servicio_choices)
    latitud = models.FloatField()
    longitud = models.FloatField()
    descripcion = models.TextField()
    disponible = models.BooleanField(default=True)

    def __str__(self):
        string = self.nombre + " " + self.apellido + \
            " (" + self.tipo_servicio + ")"
        return string
