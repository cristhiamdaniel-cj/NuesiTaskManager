# backlog/api_router.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api.views import (
    IntegranteViewSet, EpicaViewSet, SprintViewSet, TareaViewSet, matriz_eisenhower
)

router = DefaultRouter()
router.register(r'integrantes', IntegranteViewSet, basename='integrante')
router.register(r'epicas', EpicaViewSet, basename='epica')
router.register(r'sprints', SprintViewSet, basename='sprint')
router.register(r'tareas', TareaViewSet, basename='tarea')

urlpatterns = [
    path('', include(router.urls)),
    path('matriz/', matriz_eisenhower, name='matriz-eisenhower'),
]
