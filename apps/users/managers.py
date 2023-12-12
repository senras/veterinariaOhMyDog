from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):

    def create_user(self, email, nombre, apellido, telefono, direccion, password):
        if not email:
            raise ValueError(_("User debe tener un correo"))
        if not nombre:
            raise ValueError(_("User debe tener un nombre"))
        if not apellido:
            raise ValueError(_("User debe tener un apellido"))
        if not telefono:
            raise ValueError(_("User debe tener un teléfono"))
        if not direccion:
            raise ValueError(_("User debe tener una dirección"))

        email = self.normalize_email(email)
        user = self.model(email=email, nombre=nombre,
                          apellido=apellido, telefono=telefono, direccion=direccion)

        user.set_password(password)
        user.is_active = False
        user.is_superuser = False
        user.es_veterinario = False
        user.is_staff = False
        user.save(user=self._db)
        return user

    def create_superuser(self, email, nombre, apellido, telefono, direccion, password, **extra_fields):

        email = self.normalize_email(email)
        user = self.model(email=email, nombre=nombre,
                          apellido=apellido, telefono=telefono, direccion=direccion)
        user.set_password(password)
        user.is_active = True
        user.is_superuser = True
        user.es_veterinario = True
        user.is_staff = True
        user.save(using=self._db)
        return user
