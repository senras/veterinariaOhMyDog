from django import forms
from .models import Paseador_cuidador

INPUT_CLASSES = 'w-100 py-2 px-3 rounded border-0'


class RegistrarPaseador_CuidadorForm(forms.ModelForm):

    class Meta:
        model = Paseador_cuidador
        fields = ('nombre', 'apellido', 'telefono',
                  'tipo_servicio', 'mail', 'latitud', 'longitud', 'descripcion')

    nombre = forms.CharField(label="Nombre", required=True, widget=forms.TextInput(
        attrs={'class': INPUT_CLASSES}))

    apellido = forms.CharField(label="Apellido", required=True, widget=forms.TextInput(
        attrs={'class': INPUT_CLASSES}))

    telefono = forms.IntegerField(label="Teléfono", required=True, widget=forms.NumberInput(
        attrs={'class': INPUT_CLASSES, 'min': 0, 'max': 99999999999999999999}))
    # zona = forms.CharField(label="Zona", required=True, widget=forms.TextInput(
    #     attrs={'class': INPUT_CLASSES}))
    tipo_servicio = forms.CharField(label="Tipo de servicio", widget=forms.Select(
        attrs={'class': INPUT_CLASSES}, choices=[('Paseador', 'Paseador'), ('Cuidador', 'Cuidador')]))
    mail = forms.EmailField(label="Mail", required=True, widget=forms.TextInput(
        attrs={'class': INPUT_CLASSES}))

    latitud = forms.FloatField(label="Latitud", required=True, widget=forms.TextInput(
        attrs={'class': INPUT_CLASSES}))
    longitud = forms.FloatField(label="Longitud", required=True, widget=forms.TextInput(
        attrs={'class': INPUT_CLASSES}))
    descripcion = forms.CharField(
        label="Descripción", widget=forms.TextInput(attrs={'class': INPUT_CLASSES}))


class ContactarPaseadorCuidadorForm(forms.Form):

    nombre = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'nombre',
        'class': INPUT_CLASSES,
    }))
    apellido = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'apellido',
        'class': INPUT_CLASSES,
    }))
    email = forms.CharField(widget=forms.EmailInput(
        attrs={
            'placeholder': 'correo electrónico',
            'class': INPUT_CLASSES,
        }))
    telefono = forms.CharField(widget=forms.NumberInput(
        attrs={
            'placeholder': 'teléfono',
            'class': INPUT_CLASSES,
        }))
