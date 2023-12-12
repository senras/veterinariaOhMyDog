from django import forms
from .models import Turno

INPUT_CLASSES = 'w-100 py-1 px-3 rounded border-0'

class RegistrarTurno(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ('Fecha','Franja_Horaria','MotivosConsulta','Descripcion')

    Fecha = forms.CharField(widget=forms.TextInput(
        attrs={'class': INPUT_CLASSES, 'type': 'date'}))
    Franja_Horaria = forms.CharField(widget=forms.Select(
        attrs={'class': INPUT_CLASSES,},
        choices=[ ('M', 'Mañana',), ('T', 'Tarde',)]))
    Descripcion = forms.CharField(widget=forms.TextInput(
        attrs={'class': INPUT_CLASSES,}))
    MotivosConsulta = forms.CharField(widget=forms.Select(
        attrs={'class': INPUT_CLASSES,},
        choices=[ ('Castrar', 'Castrar'),
                  ('Vacunar', 'Vacunar'),
                  ('Desparasitar', 'Desparasitar'),
                  ('Consulta', 'Consulta')
                ]))
