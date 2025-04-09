from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('empleados/', include('empleados.urls')),
    path('', include('legajos.urls', namespace='legajos')),
    path('reportes/', include('reportes.urls')),
]

# Agregar manejo de archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
