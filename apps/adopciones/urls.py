from django.urls import path
from . import views

app_name = 'adopciones'

urlpatterns = [
    path('', views.mostrar_publicaciones, name='mostrar_publicaciones'),
    path('cargar_perro_adopcion/', views.cargar_perro_adopcion,
         name='cargar_perro_adopcion'),
    path('contactar_dueño_formulario/<int:id>/<str:titulo>/', views.contactar_dueño_formulario,
         name='contactar_dueño_formulario'),
    path('contactar_dueño/<int:id>/<str:titulo>/<int:publicacion_id>', views.contactar_dueño,
         name='contactar_dueño'),
    path('mis_publicaciones_adopcion/', views.mostrar_publicaciones_adopcion,
         name='mostrar_publicaciones_adopcion'),
    path('borrar_publicacion/<int:publicacion_id>/',
         views.borrar_publicacion_adopcion, name='borrar_publicacion_adopcion'),
    path('marcar_adoptado/<int:publicacion_id>/',
         views.marcar_adoptado, name='marcar_adoptado'),
    path('desmarcar_adoptado/<int:publicacion_id>/',
         views.desmarcar_adoptado, name='desmarcar_adoptado'),
]
