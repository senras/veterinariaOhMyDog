from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordChangeForm
from django.utils.translation import gettext_lazy as _

from .models import CustomUser

INPUT_CLASSES = "w-100 py-2 rounded border-0"


class LoginForm(AuthenticationForm):

    username = forms.CharField(label="Email", widget=forms.EmailInput(
        attrs={
            'placeholder': 'Correo electrónico',
            'class': INPUT_CLASSES,
        }))
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Contraseña',
            'class': INPUT_CLASSES,
        }))

    error_messages = {
        "invalid_login": _(
            "El mail o la contraseña no son correctos."
        ),
        "inactive": _("This account is inactive."),
    }


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2', 'nombre',
                  'apellido', 'direccion', 'telefono', )
        exclude = ('es_veterinario',)

    email = forms.CharField(widget=forms.EmailInput(
        attrs={
            'placeholder': 'correo electrónico',
            'class': INPUT_CLASSES,
        }))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder': 'contraseña',
            'class': INPUT_CLASSES,
        }))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder': 'contraseña',
            'class': INPUT_CLASSES,
        }))
    nombre = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'nombre',
        'class': INPUT_CLASSES,
    }))
    apellido = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'apellido',
        'class': INPUT_CLASSES,
    }))
    direccion = forms.CharField(widget=forms.TextInput(
        attrs={
            'placeholder': 'dirección',
            'class': INPUT_CLASSES,
        }))
    telefono = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'placeholder': 'teléfono',
            'class': INPUT_CLASSES,
        }))
    es_veterinario = forms.BooleanField(
        required=False, widget=forms.CheckboxInput())

    def clean_email(self):
        email = self.cleaned_data['email']
        users = CustomUser.objects.filter(email__iexact=email)
        if users:
            raise forms.ValidationError("El email ya se encuentra en uso.")
        return email.lower()

    error_messages = {
        'password_mismatch': 'Las contraseñas ingresadas no coinciden.',
    }


class CustomUserChangeInfoFormAdmin(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'direccion', 'telefono',
                  'nombre', 'apellido', 'es_veterinario')

    email = forms.CharField(required=False, widget=forms.EmailInput(
        attrs={'placeholder': 'Correo electrónico',
               'class': INPUT_CLASSES,
               }))
    password = forms.CharField(required=False, widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Contraseña',
            'class': INPUT_CLASSES,
        }))
    nombre = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'nombre',
        'class': INPUT_CLASSES,
    }))
    apellido = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'apellido',
        'class': INPUT_CLASSES,
    }))
    direccion = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Dirección',
               'class': INPUT_CLASSES,
               }))
    telefono = forms.IntegerField(required=False, widget=forms.NumberInput(
        attrs={
            'placeholder': 'Teléfono',
            'class': INPUT_CLASSES,
        }))
    es_veterinario = forms.BooleanField(
        required=False, widget=forms.CheckboxInput())


class CustomUserChangeInfoForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'direccion', 'telefono',)

    email = forms.CharField(required=False, widget=forms.EmailInput(
        attrs={'placeholder': 'Correo electrónico',
               'class': INPUT_CLASSES,
               }))
    direccion = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Dirección',
               'class': INPUT_CLASSES,
               }))
    telefono = forms.IntegerField(required=False, widget=forms.NumberInput(
        attrs={
            'placeholder': 'Teléfono',
            'class': INPUT_CLASSES,
        }))

    def clean_email(self):
        email = self.cleaned_data['email']
        users = CustomUser.objects.filter(email__iexact=email)
        if users:
            raise forms.ValidationError("El email ya se encuentra en uso.")
        return email.lower()


class RecoverAccountForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(
        attrs={'placeholder': 'Tu dirección de correo electrónico',
               'class': INPUT_CLASSES,
               }))


class CustomUserChangePasswordForm(PasswordChangeForm):
    class Meta:
        model = CustomUser
        fields = ('old_password', 'new_password1', 'new_password2')
    old_password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder': 'contraseña actual',
            'class': 'w-75 py-2 rounded border-0',
        }))

    new_password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder': 'contraseña',
            'class': 'w-75 py-2 rounded border-0',
        }))
    new_password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder': 'contraseña',
            'class': 'w-75 py-2 rounded border-0',
        }))

    error_messages = {
        'password_incorrect': 'La contraseña ingresada no es correcta.',
        'password_mismatch': 'Las contraseñas ingresadas no coinciden.',
    }
