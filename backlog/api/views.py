from rest_framework import viewsets, mixins
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models import Integrante, Epica, Sprint, Tarea, Evidencia
from .serializers import IntegranteSerializer, EpicaSerializer, SprintSerializer, TareaSerializer, EvidenciaSerializer
from .permissions import IsBacklogAdmin, IsOwnerOrAdmin

class IntegranteViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = IntegranteSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Integrante.objects.select_related("user").all().order_by("user__first_name","user__last_name")

class EpicaViewSet(viewsets.ModelViewSet):
    serializer_class = EpicaSerializer
    permission_classes = [IsAuthenticated, IsBacklogAdmin]
    queryset = Epica.objects.select_related("owner").all().order_by("-creada_en")

class SprintViewSet(viewsets.ModelViewSet):
    serializer_class = SprintSerializer
    permission_classes = [IsAuthenticated, IsBacklogAdmin]
    queryset = Sprint.objects.all().order_by("inicio")

class TareaViewSet(viewsets.ModelViewSet):
    serializer_class = TareaSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    queryset = Tarea.objects.select_related("asignado_a__user","sprint","epica").all().order_by("sprint__inicio","categoria","id")

    def get_queryset(self):
        qs = super().get_queryset()
        i = getattr(self.request.user, "integrante", None)
        persona = self.request.query_params.get("persona")
        sprint = self.request.query_params.get("sprint")
        epica = self.request.query_params.get("epica")
        estado = self.request.query_params.get("estado")
        mine = self.request.query_params.get("mine")

        if not (i and i.puede_crear_tareas()):
            qs = qs.filter(asignado_a=i)

        if persona: qs = qs.filter(asignado_a_id=persona)
        if sprint: qs = qs.filter(sprint_id=sprint)
        if epica: qs = qs.filter(epica_id=epica)
        if estado == "abiertas": qs = qs.filter(completada=False)
        elif estado == "cerradas": qs = qs.filter(completada=True)
        if mine == "1": qs = qs.filter(asignado_a=i)
        return qs

    @action(methods=["patch"], detail=True, url_path="categoria")
    def cambiar_categoria(self, request, pk=None):
        tarea = self.get_object()
        categoria = (request.data.get("categoria") or "").upper()
        validas = {c[0] for c in Tarea.MATRIZ_CHOICES}
        if categoria not in validas:
            return Response({"detail":"Categoria inválida"}, status=400)
        tarea.categoria = categoria
        tarea.save(update_fields=["categoria"])
        return Response({"ok": True, "categoria": tarea.categoria})

    @action(methods=["patch"], detail=True, url_path="estado")
    def cambiar_estado(self, request, pk=None):
        tarea = self.get_object()
        estado = (request.data.get("estado") or "").upper()
        validos = {c[0] for c in Tarea.ESTADO_CHOICES}
        if estado not in validos:
            return Response({"detail":"Estado inválido"}, status=400)
        tarea.estado = estado
        if estado == "COMPLETADO":
            tarea.completada = True
        tarea.save(update_fields=["estado","completada"])
        return Response({"ok": True, "estado": tarea.estado})

    @action(methods=["post"], detail=True, url_path="evidencias", permission_classes=[IsAuthenticated])
    def crear_evidencia(self, request, pk=None):
        tarea = self.get_object()
        serializer = EvidenciaSerializer(data=request.data)
        if serializer.is_valid():
            ev = serializer.save(tarea=tarea, creado_por=request.user)
            return Response(EvidenciaSerializer(ev).data, status=201)
        return Response(serializer.errors, status=400)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def matriz_eisenhower(request):
    i = getattr(request.user, "integrante", None)
    base = Tarea.objects.select_related("asignado_a__user","sprint","epica").order_by("sprint__inicio","id")
    if not (i and i.puede_crear_tareas()):
        base = base.filter(asignado_a=i)

    for key, field in [("persona","asignado_a_id"),("sprint","sprint_id"),("epica","epica_id")]:
        val = request.query_params.get(key)
        if val: base = base.filter(**{field: val})
    if request.query_params.get("mine") == "1":
        base = base.filter(asignado_a=i)

    ser = lambda qs: TareaSerializer(qs, many=True).data
    return Response({
        "ui": ser(base.filter(categoria="UI")),
        "nui": ser(base.filter(categoria="NUI")),
        "uni": ser(base.filter(categoria="UNI")),
        "nuni": ser(base.filter(categoria="NUNI")),
    })
