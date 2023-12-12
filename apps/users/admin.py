from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeInfoForm
from .models import CustomUser

# es_veterinario
# is_active
# is_superuser
# is_staff
# nombre
# apellido
# telefono
# direccion


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeInfoForm
    model = CustomUser
    list_display = ("is_active", "es_veterinario", "is_staff",
                    "email", "nombre", "apellido", "telefono", "direccion")
    list_editable = ("es_veterinario", "is_staff",
                     "email", "nombre", "apellido", "telefono", "direccion")
    list_filter = ("is_staff", "es_veterinario", "is_active",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (("Información personal"), {
         "fields": ("nombre", "apellido", "telefono", "direccion")}),
        ("Permissions", {"fields": ("is_staff", "es_veterinario", "is_superuser",
         "is_active")}),
    )
    add_fieldsets = (
        (None, {'fields': ("email", "password1", "password2",
         "nombre", "apellido", "telefono", "direccion",)}),
        ('Permissions', {"fields": ("is_staff", "es_veterinario", "is_superuser",
         "is_active")}),
    )
    search_fields = ("email",)
    ordering = ("email",)

    def get_fieldsets(self, request, obj=None):
        if not request.user.is_superuser:
            if obj:
                if isinstance(obj, CustomUser):
                    fieldsets = (
                        (None, {"fields": ("email", "password")}),
                        (("Información personal"), {
                         "fields": ("nombre", "apellido", "telefono", "direccion")}),
                        ("Permissions", {"fields": (
                            "is_staff", "es_veterinario", "is_superuser", "is_active")}),
                    )
                    return fieldsets
            else:
                return self.add_fieldsets
        else:
            if obj:
                if isinstance(obj, CustomUser):
                    return self.fieldsets
            else:
                return self.add_fieldsets

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ('last_login', 'date_joined')
        else:
            return self.readonly_fields


admin.site.register(CustomUser, CustomUserAdmin)
