from django.urls import path, include

urlpatterns = [
    path("api/backlog/", include("backlog.urls")),
    # ... el resto de tus rutas de otros apps
]
