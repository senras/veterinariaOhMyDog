from django.urls import path
from . import views

app_name = 'colectas'

urlpatterns = [
    path('', views.mostrar_colectas, name='mostrar_colectas'),
    path('nueva_colecta/', views.nueva_colecta, name='nueva_colecta'),
    path('borrar_colecta/<int:colecta_id>/',
         views.borrar_colecta, name='borrar_colecta'),
    path('marcar_concluida/<int:colecta_id>/',
         views.marcar_concluida, name='marcar_concluida'),
    path('desmarcar_concluida/<int:colecta_id>/',
         views.desmarcar_concluida, name='desmarcar_concluida'),

    path('pantalla_donacion/<int:colecta_id>/',
         views.pantalla_donacion, name='pantalla_donacion'),
    path('donar_colecta/<int:colecta_id>/<int:monto>/',
         views.donar_colecta, name='donar_colecta'),
    path('mostrar_detalle_colecta/<int:colecta_id>/',
         views.mostrar_detalle_colecta, name='mostrar_detalle_colecta'),
    path('success/', views.success, name='success'),
    path('failure/', views.failure, name='failure'),
    path('pending/', views.pending, name='pending'),
    path('notification/', views.notification, name='notification'),

]
