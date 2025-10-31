# -*- coding: utf-8 -*-
from datetime import datetime
import json
from django.db.models import Q
from django.utils.timezone import now
from rest_framework import viewsets, mixins
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import Integrante, Proyecto, Epica, Sprint, Tarea, Evidencia
from .serializers import (
    IntegranteSerializer, ProyectoSerializer, EpicaSerializer,
    SprintSerializer, TareaSerializer, EvidenciaSerializer
)
from .permissions import IsBacklogAdmin, IsOwnerOrAdmin
from .mixins import EnvelopeMixin  # <<< mixin de envelope


# ===== Helpers de scope (visualizador por proyectos) =====
def _proyectos_autorizados_qs(integrante):
    if not integrante:
        return Proyecto.objects.none()
    if integrante.es_admin():
        return Proyecto.objects.all()
    if integrante.es_visualizador():
        return Proyecto.objects.filter(
            permisos_integrantes__integrante=integrante,
            permisos_integrantes__activo=True,
            activo=True
        ).distinct()
    return Proyecto.objects.none()


def _filtrar_tareas_por_scope(qs, integrante):
    """Restringe Tarea por proyectos autorizados a visualizador; miembros ven solo las suyas."""
    if not integrante:
        return qs.none()
    if integrante.es_admin():
        return qs
    if integrante.es_visualizador():
        proys = _proyectos_autorizados_qs(integrante)
        if not proys.exists():
            return qs.none()
        return qs.filter(epica__proyecto__in=proys).distinct()
    # miembro normal -> OR sin union()
    return qs.filter(Q(asignados=integrante) | Q(asignado_a=integrante)).distinct()

# ===== ViewSets =====
class IntegranteViewSet(EnvelopeMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = IntegranteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Integrante.objects
            .select_related("user")
            .all()
            .order_by("user__first_name", "user__last_name")
        )


class ProyectoViewSet(EnvelopeMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = ProyectoSerializer
    permission_classes = [IsAuthenticated]
    queryset = Proyecto.objects.all().order_by("codigo")


class EpicaViewSet(EnvelopeMixin, viewsets.ModelViewSet):
    serializer_class = EpicaSerializer
    permission_classes = [IsAuthenticated, IsBacklogAdmin]
    queryset = (
        Epica.objects
        .select_related("owner", "proyecto")
        .prefetch_related("owners__user", "sprints")
        .all()
        .order_by("-creada_en")
    )


class SprintViewSet(EnvelopeMixin, viewsets.ModelViewSet):
    serializer_class = SprintSerializer
    permission_classes = [IsAuthenticated, IsBacklogAdmin]
    queryset = Sprint.objects.all().order_by("inicio")


class TareaViewSet(EnvelopeMixin, viewsets.ModelViewSet):
    serializer_class = TareaSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    queryset = (
        Tarea.objects
        .select_related("asignado_a__user", "sprint", "epica", "epica__proyecto")
        .prefetch_related("asignados__user")
        .all()
        .order_by("sprint__inicio", "categoria", "id")
    )
    def get_queryset(self):
        qs = super().get_queryset()
        i = getattr(self.request.user, "integrante", None)
        qs = _filtrar_tareas_por_scope(qs, i)

        qp = self.request.query_params
        if qp.get("persona"):
            pid = qp["persona"]
            qs = qs.filter(Q(asignado_a_id=pid) | Q(asignados__id=pid))
        if qp.get("sprint"):
            qs = qs.filter(sprint_id=qp["sprint"])
        if qp.get("epica"):
            qs = qs.filter(epica_id=qp["epica"])

        estado = qp.get("estado")
        if estado == "abiertas":
            qs = qs.filter(completada=False)
        elif estado == "cerradas":
            qs = qs.filter(completada=True)

        if qp.get("mine") == "1" and i:
            qs = qs.filter(Q(asignados=i) | Q(asignado_a=i))

        return qs.distinct()

    # ----- Acciones Kanban / Matriz -----
    @action(methods=["patch"], detail=True, url_path="categoria")
    def cambiar_categoria(self, request, pk=None):
        tarea = self.get_object()
        categoria = (request.data.get("categoria") or "").upper()
        validas = {c[0] for c in Tarea.MATRIZ_CHOICES}
        if categoria not in validas:
            return Response(
                {"ok": False, "error": {"code": "validation_error", "detail": "Categoría inválida"}},
                status=400
            )
        tarea.categoria = categoria
        tarea.save(update_fields=["categoria"])
        return Response({"ok": True, "data": TareaSerializer(tarea).data}, status=200)

    @action(methods=["patch"], detail=True, url_path="estado")
    def cambiar_estado(self, request, pk=None):
        tarea = self.get_object()
        estado = (request.data.get("estado") or "").upper()
        validos = {c[0] for c in Tarea.ESTADO_CHOICES}
        if estado not in validos:
            return Response(
                {"ok": False, "error": {"code": "validation_error", "detail": "Estado inválido"}},
                status=400
            )

        tarea.estado = estado
        if estado == "COMPLETADO":
            tarea.completada = True
            if not tarea.fecha_cierre:
                tarea.fecha_cierre = now()
            tarea.save(update_fields=["estado", "completada", "fecha_cierre"])
        else:
            tarea.save(update_fields=["estado"])

        return Response({"ok": True, "data": TareaSerializer(tarea).data}, status=200)

    @action(methods=["post"], detail=True, url_path="evidencias", permission_classes=[IsAuthenticated])
    def crear_evidencia(self, request, pk=None):
        tarea = self.get_object()
        serializer = EvidenciaSerializer(data=request.data)
        if serializer.is_valid():
            ev = serializer.save(tarea=tarea, creado_por=request.user)
            return Response({"ok": True, "data": EvidenciaSerializer(ev).data}, status=201)
        return Response(
            {"ok": False, "error": {"code": "validation_error", "fields": serializer.errors}},
            status=400
        )


# ----- Matriz (colección) -----
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def matriz_eisenhower(request):
    i = getattr(request.user, "integrante", None)
    base = (
        Tarea.objects
        .select_related("asignado_a__user", "sprint", "epica", "epica__proyecto")
        .prefetch_related("asignados__user")
        .order_by("sprint__inicio", "id")
    )
    base = _filtrar_tareas_por_scope(base, i)

    for key, field in [("persona", "asignado_a_id"), ("sprint", "sprint_id"), ("epica", "epica_id")]:
        val = request.query_params.get(key)
        if val:
            base = base.filter(**{field: val})
    if request.query_params.get("mine") == "1" and i:
        base = base.filter(asignados=i) | base.filter(asignado_a=i)

    ser = lambda qs: TareaSerializer(qs.distinct(), many=True).data
    payload = {
        "ui": ser(base.filter(categoria="UI")),
        "nui": ser(base.filter(categoria="NUI")),
        "uni": ser(base.filter(categoria="UNI")),
        "nuni": ser(base.filter(categoria="NUNI")),
    }
    return Response({"ok": True, "data": payload, "meta": None}, status=200)
