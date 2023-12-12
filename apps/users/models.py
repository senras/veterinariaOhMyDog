from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    date_joined = models.DateTimeField(
        verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    es_veterinario = models.BooleanField(_("es_veterinario"), default=False)
    is_active = models.BooleanField(_("active"), default=True)
    is_superuser = models.BooleanField(_("superuser"), default=False)
    is_staff = models.BooleanField(_("staff"), default=False)
    nombre = models.CharField(_("nombre"), max_length=50)
    apellido = models.CharField(_("apellido"), max_length=50)
    telefono = models.IntegerField(_("telefono"))
    direccion = models.CharField(_("direccion"), max_length=50)
    publicaciones_contactadas = models.JSONField(
        _("publicaciones_contactadas"), default=dict)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ["-date_joined"]
    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.es_veterinario

    def has_module_perms(self, app_label):
        return True
