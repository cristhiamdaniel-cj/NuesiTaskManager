from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth JSON (csrf / login / me / logout)
    path('api/backlog/auth/', include('backlog.api_urls')),

    # DRF (router)
    path('api/backlog/', include('backlog.api_router')),  # 👈 aquí
]
