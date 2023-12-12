from django.db import models
from apps.users.models import CustomUser


class Colecta(models.Model):

    def __str__(self):
        return self.titulo

    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    monto_meta = models.FloatField()
    monto_recaudado = models.FloatField(default=0)
    porcentaje = models.TextField()
    fecha_limite = models.DateField(auto_now=False, auto_now_add=False)
    concluida = models.BooleanField(default=False)



class Donacion(models.Model):
    monto = models.FloatField()
    email = models.EmailField(verbose_name="email", max_length=60, null=True, blank=True, unique=False)
    fecha = models.DateTimeField(auto_now_add=True)
    donador = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    colecta = models.ForeignKey(Colecta, on_delete=models.CASCADE)

    class Meta:
        ordering = ('fecha',)

class EmailDonacionHardcode(models.Model):
    email = models.EmailField(verbose_name="email", max_length=60, unique=False)
    colecta = models.ForeignKey(Colecta, on_delete=models.CASCADE)
