from django.urls import path
from . import views

app_name = 'encontrados'

urlpatterns = [
    path('', views.ver_encontrados, name='ver_encontrados'),
    path('ver_mis_encontrados/', views.ver_mis_encontrados,
         name='ver_mis_encontrados'),
    path('cargar_perro_encontrado/', views.cargar_perro_encontrado,
         name='cargar_perro_encontrado'),
    path('contactar_dueño_formulario/<int:id_dueño>/<int:publicacion_id>/', views.contactar_dueño_formulario, name='contactar_dueño_formulario'),
    path('contactar_dueño/<int:id>/<int:publicacion_id>/', views.contactar_dueño, name='contactar_dueño'),
    path('borrar_encontrado/<int:publicacion_id>/',
         views.borrar_encontrado, name='borrar_encontrado'),
    path('marcar_ubicado/<int:publicacion_id>/',
         views.marcar_ubicado, name='marcar_ubicado'),
    path('desmarcar_ubicado/<int:publicacion_id>/',
         views.desmarcar_ubicado, name='desmarcar_ubicado'),
]
