from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Vistas HTML mientras migramos
    path('', include('backlog.urls')),
    path('disponibilidad/', include('disponibilidad.urls')),

    # API de auth dentro de backlog
    path('api/auth/', include('backlog.api_urls')),

    # API DRF del Backlog (Matriz, Tareas, etc.)
    path("api/backlog/", include("backlog.api.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
