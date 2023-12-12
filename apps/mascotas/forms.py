from django import forms
from .models import Perro, HistoriaClinica, LibretaVacunas
from datetime import date, timedelta

INPUT_CLASSES = 'w-100 py-1 px-3 rounded border-0'

yesterday = today = date.today() - timedelta(days=1)


class RegistrarMascotaForm(forms.ModelForm):
    class Meta:
        model = Perro
        fields = ('nombre', 'raza', 'color', 'castrado',
                  'sexo', 'tamaño', 'fecha_nacimiento')

    nombre = forms.CharField(widget=forms.TextInput(
        attrs={'class': INPUT_CLASSES}))
    raza = forms.CharField(widget=forms.TextInput(
        attrs={'class': INPUT_CLASSES}))
    color = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': INPUT_CLASSES}))
    castrado = forms.BooleanField(widget=forms.CheckboxInput(
        attrs={'class': INPUT_CLASSES, 'required': False, 'initial': False, })),
    sexo = forms.CharField(widget=forms.Select(attrs={'class': INPUT_CLASSES},
                                               choices=[('M', 'Macho'), ('H', 'Hembra')]))
    tamaño = forms.CharField(widget=forms.Select(attrs={'class': INPUT_CLASSES},
                                                  choices=[('Chico', 'Chico'), ('Mediano', 'Mediano'), ('Grande', 'Grande')]))
    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(attrs={'max': str(yesterday), 'class': INPUT_CLASSES, 'type': 'date', 'default': str(yesterday)},))


class RegistrarHistoriaForm(forms.ModelForm):
    class Meta:
        model = HistoriaClinica
        fields = ('fecha', 'peso', 'descripcion', 'diagnostico')

    fecha = forms.CharField(widget=forms.TextInput(
        attrs={'class': INPUT_CLASSES, 'type': 'date'}))
    peso = forms.FloatField(widget=forms.NumberInput(
        attrs={'class': INPUT_CLASSES}))
    descripcion = forms.CharField(widget=forms.TextInput(
        attrs={'class': INPUT_CLASSES}))
    diagnostico = forms.CharField(widget=forms.TextInput(
        attrs={'class': INPUT_CLASSES}))


class RegistarCastracionForm(forms.ModelForm):
    class Meta:
        model = HistoriaClinica
        fields = ('fecha', 'peso', 'descripcion')

    fecha = forms.DateField(widget=forms.TextInput(
        attrs={'class': INPUT_CLASSES, 'type': 'date'}))
    peso = forms.FloatField(widget=forms.NumberInput(
        attrs={'class': INPUT_CLASSES}))
    descripcion = forms.CharField(widget=forms.TextInput(
        attrs={'class': INPUT_CLASSES}))


class RegistrarVacunaForm(forms.ModelForm):
    class Meta:
        model = LibretaVacunas
        fields = ('fecha', 'marca', 'tipo', 'lote', 'numero_dosis')

    fecha = forms.DateField(widget=forms.TextInput(
        attrs={'class': INPUT_CLASSES, 'type': 'date'}))
    marca = forms.CharField(widget=forms.TextInput(
        attrs={'class': INPUT_CLASSES}))
    lote = forms.CharField(widget=forms.TextInput(
        attrs={'class': INPUT_CLASSES}))
    tipo = forms.CharField(widget=forms.Select(
        choices=[('M', 'Moquillo'), ('A', 'Antirrabica')]))
    numero_dosis = forms.FloatField(widget=forms.NumberInput(
        attrs={'class': INPUT_CLASSES}))
