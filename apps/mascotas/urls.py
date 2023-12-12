from django.urls import path
from . import views

app_name = 'mascotas'

urlpatterns = [
     path('ver_perros/<int:id>', views.ver_perros, name='ver_perros'),
     path('ver_mis_perros/', views.ver_mis_perros, name='ver_mis_perros'),
     path('historia_clinica/<int:id>', views.historia_clinica, name='historia_clinica'),
     path('vacunas/<int:id>', views.vacunas, name='vacunas'),
     path('registrar_mascota/<int:id>', views.registrar_mascota, name='registrar_mascota'),
     path('agregar_historia_clinica/<int:id>', views.agregar_historia_clinica, name='agregar_historia_clinica'),
     path('registrar_vacuna/<int:id>/', views.registrar_vacuna, name='registrar_vacuna'),
     path('borrar_vacuna/<int:id_perro>/<int:id_vacuna>', views.borrar_vacuna, name='borrar_vacuna'),
     path('borrar_historia/<int:id_perro>/<int:id_historia>/', views.borrar_historia, name='borrar_historia'),
     path('registrar_castracion/<int:id_perro>/', views.registrar_castracion, name='registrar_castracion'),
]
