from django import forms
from .models import PublicacionPerroPerdido

INPUT_CLASSES = 'w-100 py-2 px-3 rounded border-0'


class RegistrarPerroPerdido(forms.ModelForm):
    class Meta:
        model = PublicacionPerroPerdido
        fields = ('titulo', 'nombre', 'zona', 'tamaño', 'rango_edad', 'descripcion',
                  'raza', 'color', 'sexo', 'imagen',)
        exclude = ('usuario', 'encontrado')

    titulo = forms.CharField(label="Título", max_length=200,
                             required=True, widget=forms.TextInput(attrs={'class': INPUT_CLASSES}))
    nombre = forms.CharField(label="Nombre", max_length=200,
                             required=True, widget=forms.TextInput(attrs={'class': INPUT_CLASSES}))

    zona = forms.CharField(label="Zona", max_length=200,
                           required=True, widget=forms.TextInput(attrs={'class': INPUT_CLASSES}))

    tamaño = forms.CharField(label="Tamaño", widget=forms.Select(attrs={'class': INPUT_CLASSES}, choices=[('Chico', 'Chico'), ('Mediano', 'Mediano'), ('Grande', 'Grande')]))

    rango_edad = forms.CharField(label="Edad", widget=forms.Select(attrs={'class': INPUT_CLASSES},
        choices=[('Cachorro', 'Cachorro'), ('Joven', 'Joven'), ('Adulto', 'Adulto')]))

    descripcion = forms.CharField(label="Descripción", required=True,
        widget=forms.TextInput(attrs={'class': INPUT_CLASSES}))

    raza = forms.CharField(label="Raza", max_length=100, required=False,
        widget=forms.TextInput(attrs={'class': INPUT_CLASSES}))

    color = forms.CharField(label="Color", max_length=100, required=False,
        widget=forms.TextInput(attrs={'class': INPUT_CLASSES}))

    sexo = forms.CharField(label="Sexo", required=False, widget=forms.TextInput(attrs={'class': INPUT_CLASSES}))

    imagen = forms.ImageField(label="Imagen", required=False, widget=forms.FileInput(attrs={'class': INPUT_CLASSES}))

    def clean(self):
        cleaned_data = super().clean()
        titulo = cleaned_data.get("titulo")
        zona = cleaned_data.get("zona")
        descripcion = cleaned_data.get("descripcion")

        if not titulo:
            self.add_error('titulo', 'El titulo es obligatorio')

        if not zona:
            self.add_error('zona', 'La zona es obligatoria')

        if not descripcion:
            self.add_error('descripcion', 'La descripcion es obligatoria')

        return cleaned_data


class ContactarNoRegistrado(forms.Form):

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
