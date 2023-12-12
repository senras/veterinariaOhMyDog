from django.urls import path
from . import views

app_name = 'perdidos'

urlpatterns = [
    path('', views.ver_perdidos, name='ver_perdidos'),
    path('ver_mis_perdidos/', views.ver_mis_perdidos, name='ver_mis_perdidos'),
    path('cargar_perro_perdido/', views.cargar_perro_perdido,
         name='cargar_perro_perdido'),
    path('contactar_dueño_formulario/<int:id_dueño>/<int:publicacion_id>/', views.contactar_dueño_formulario, name='contactar_dueño_formulario'),
    path('contactar_dueño/<int:id>/<int:publicacion_id>/', views.contactar_dueño, name='contactar_dueño'),
    path('borrar_perdido/<int:publicacion_id>/',
         views.borrar_perdido, name='borrar_perdido'),
    path('marcar_encontrado/<int:publicacion_id>/',
         views.marcar_encontrado, name='marcar_encontrado'),
    path('desmarcar_encontrado/<int:publicacion_id>/', views.desmarcar_encontrado,
         name='desmarcar_encontrado'),
]
