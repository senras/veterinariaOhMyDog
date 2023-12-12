from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", include("apps.users.urls")),
    path('admin/', admin.site.urls),
    path('adopciones/', include('apps.adopciones.urls')),
    path('mascotas/', include('apps.mascotas.urls')),
    path('colectas/', include('apps.colectas.urls')),
    path('turnos/', include('apps.turnos.urls')),
    path('perdidos/', include('apps.perdidos.urls')),
    path('encontrados/', include('apps.encontrados.urls')),
    path('mapa/', include('apps.mapa.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
