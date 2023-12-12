from django import forms
from datetime import date
from datetime import timedelta

mañana = today = date.today() + timedelta(days=1)


class NuevaColecta(forms.Form):
    titulo = forms.CharField(label='Título', max_length=150, required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    descripcion = forms.CharField(label='Descripción', max_length=250,
                                  required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    monto_meta = forms.DecimalField(label='Monto meta', required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'min': 1}), error_messages={'invalid': 'Ingrese un número válido para el monto meta.'})

    fecha_limite = forms.DateField(
        label='Fecha límite', required=True, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'min': str(mañana)}))

    def clean(self):
        cleaned_data = super().clean()
        monto_meta = cleaned_data.get('monto_meta')
        if monto_meta:
            try:
                float(monto_meta)
            except ValueError:
                self.add_error(
                    'monto_meta', 'Ingrese un número válido para el monto meta.')

        fecha_seleccionada = cleaned_data.get('fecha_limite')
        if fecha_seleccionada and fecha_seleccionada < date.today():
            self.add_error(
                'fecha_limite', 'No se permiten fechas anteriores a la fecha actual.')


class NuevaDonacion(forms.Form):

    monto = forms.DecimalField(label='Monto', min_value=1, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control'}), error_messages={'invalid': 'Ingrese un número válido para el monto.'})
    
    mail = forms.EmailField(label='Correo electrónico', max_length=150, required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
