# backlog/urls.py  (solo API)
from django.urls import path, include

urlpatterns = [
    path("auth/", include(("backlog.api_urls", "api_backlog_auth"), namespace="api_backlog_auth")),
    path("", include("backlog.api_router")),   # router DRF (integrantes/epicas/sprints/tareas/matriz)
]
