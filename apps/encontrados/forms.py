from django import forms
from .models import PublicacionPerroEncontrado

INPUT_CLASSES = 'w-100 py-2 px-3 rounded border-0'


class RegistrarPerroEncontrado(forms.ModelForm):
    class Meta:
        model = PublicacionPerroEncontrado
        fields = ('titulo', 'zona', 'raza', 'sexo', 'tamaño', 'rango_edad', 'descripcion',
                  'color',  'imagen', )
        exclude = ('usuario', 'ubicado')

    titulo = forms.CharField(label="Título", required=True, widget=forms.TextInput(attrs={
        'class': INPUT_CLASSES}))

    zona = forms.CharField(label="Zona", required=True, widget=forms.TextInput(
        attrs={'class': INPUT_CLASSES}))

    raza = forms.CharField(label="Raza", required=False, widget=forms.TextInput(attrs={'class': INPUT_CLASSES}))

    sexo = forms.CharField(label="Sexo", required=False, widget=forms.TextInput(attrs={'class': INPUT_CLASSES}))

    tamaño = forms.CharField(label="Tamaño", widget=forms.Select(attrs={'class': INPUT_CLASSES}, choices=[('Chico', 'Chico'), ('Mediano', 'Mediano'), ('Grande', 'Grande')]))

    rango_edad = forms.CharField(label="Edad", widget=forms.Select(attrs={'class': INPUT_CLASSES}, choices=[('Cachorro', 'Cachorro'), ('Joven', 'Joven'), ('Adulto', 'Adulto')]))

    descripcion = forms.CharField(label="Descripción", required=True,
        widget=forms.TextInput(attrs={'class': INPUT_CLASSES}))
        
    imagen = forms.ImageField(label="Imagen", required=False)

    color = forms.CharField(label="Color", max_length=100, required=False,
        widget=forms.TextInput(attrs={'class': INPUT_CLASSES}))

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
