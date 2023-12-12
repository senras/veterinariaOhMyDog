from django.urls import path
from . import views

app_name = 'turnos'

urlpatterns = [
    path('', views.turnos_main),
    path('mostrar_turnos/', views.ver_turnos, name='mostrar_turnos'),
    path('solicitar_turno/', views.pedir_turno, name='solicitar_turno'),
    path('turnos_pendientes/', views.ver_turnos_pendientes, name='turnos_pendientes'),
    path('aceptar_turno/<int:id>/', views.aceptar_turno, name='aceptar_turno'),
    path('rechazar_turno/<int:id>/', views.rechazar_turno, name='rechazar_turno'),

    path('mis_turnos/', views.mis_turnos, name='mis_turnos'),
]