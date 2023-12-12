from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import LoginForm

app_name = 'users'

urlpatterns = [
    path("", views.index, name="index"),
    path("crear_cliente/", views.crear_cliente, name="crear_cliente"),
    path('login/', auth_views.LoginView.as_view(template_name='login.html',
                                                authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.logout_then_login, name='logout'),
    path('cambiar_contraseña/', views.cambiar_contraseña, name='cambiar_contraseña'),
    path('cambiar_info/', views.cambiar_info, name='cambiar_info'),
    path('mi_perfil/', views.mi_perfil, name='mi_perfil'),
    path('recuperar_cuenta/', views.recuperar_cuenta, name='recuperar_cuenta'),
    path('mostrar_usuarios/', views.mostrar_usuarios, name='mostrar_usuarios'),
    path('mostrar_perfil/<int:id>/', views.mostrar_perfil, name='mostrar_perfil'),
]
