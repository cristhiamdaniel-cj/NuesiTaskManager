# backlog/urls.py  (solo API)
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("auth/", include(("backlog.api_urls", "api_backlog_auth"), namespace="api_backlog_auth")),
    path("", include("backlog.api_router")),   # router DRF (integrantes/epicas/sprints/tareas/matriz)
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]
