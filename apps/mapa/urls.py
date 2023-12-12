from django.urls import path
from . import views

app_name = 'mapa'

urlpatterns = [
    path('mostrar_mapa_veterinario/', views.mostrar_mapa_veterinario,
         name='mostrar_mapa_veterinario'),
    path('mostrar_mapa_usuario/', views.mostrar_mapa_usuario,
         name='mostrar_mapa_usuario'),

    path('registrar_paseador_cuidador/', views.registrar_paseador_cuidador,
         name='registrar_paseador_cuidador/'),
    path('borrar_paseador_cuidador/<int:id>', views.borrar_paseador_cuidador,
         name="borrar_paseador_cuidador"),
    path('modificar_paseador_cuidador/<int:id>',
         views.modificar_paseador_cuidador, name="modificar_paseador_cuidador"),
    path('marcar_disponible/<int:id>',
         views.marcar_disponible, name="marcar_disponible"),
    path('marcar_no_disponible/<int:id>',
         views.marcar_no_disponible, name="marcar_no_disponible"),
    path('contactar/<int:id>', views.contactar, name="contactar"),
]
