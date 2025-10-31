from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth JSON (csrf / login / me / logout)
    path('api/backlog/auth/', include('backlog.api_urls')),

    # DRF (router)
    path('api/backlog/', include('backlog.api_router')),  

    # 👇 rutas de OpenAPI/Swagger en el raíz del proyecto
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
