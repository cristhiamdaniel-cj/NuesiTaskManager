from rest_framework import serializers
from django.contrib.auth.models import User
from ..models import (
    Integrante, Proyecto, Epica, Sprint, Tarea, Evidencia
)

# -------- Users / Integrantes --------
class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email")

class IntegranteSerializer(serializers.ModelSerializer):
    user = UserMiniSerializer()
    class Meta:
        model = Integrante
        fields = ("id", "rol", "user")

# -------- Proyecto / Sprint --------
class ProyectoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proyecto
        fields = ("id", "codigo", "nombre", "activo")

class SprintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sprint
        fields = ("id", "nombre", "inicio", "fin")

# -------- Épica --------
class EpicaSerializer(serializers.ModelSerializer):
    proyecto = ProyectoSerializer(read_only=True)
    proyecto_id = serializers.PrimaryKeyRelatedField(
        queryset=Proyecto.objects.all(), source="proyecto",
        write_only=True, required=True
    )

    owner = IntegranteSerializer(read_only=True)
    owner_id = serializers.PrimaryKeyRelatedField(
        queryset=Integrante.objects.all(), source="owner",
        write_only=True, required=False, allow_null=True
    )

    # Owners M2M (opcional)
    owners = IntegranteSerializer(many=True, read_only=True)
    owners_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Integrante.objects.all(), source="owners",
        write_only=True, required=False
    )

    sprints = SprintSerializer(many=True, read_only=True)
    sprints_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Sprint.objects.all(), source="sprints",
        write_only=True, required=False
    )

    class Meta:
        model = Epica
        fields = (
            "id", "codigo", "titulo", "descripcion",
            "proyecto", "proyecto_id",
            "owner", "owner_id",
            "owners", "owners_ids",
            "prioridad", "estado", "avance",
            "sprints", "sprints_ids",
            "kpis", "creada_en", "actualizada_en",
        )

# -------- Tarea / Evidencia --------
class TareaSerializer(serializers.ModelSerializer):
    asignado_a = IntegranteSerializer(read_only=True)
    asignado_a_id = serializers.PrimaryKeyRelatedField(
        queryset=Integrante.objects.all(), source="asignado_a",
        write_only=True, required=False, allow_null=True
    )

    # M2M asignados
    asignados = IntegranteSerializer(many=True, read_only=True)
    asignados_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Integrante.objects.all(), source="asignados",
        write_only=True, required=False
    )

    sprint = SprintSerializer(read_only=True)
    sprint_id = serializers.PrimaryKeyRelatedField(
        queryset=Sprint.objects.all(), source="sprint",
        write_only=True, required=False, allow_null=True
    )

    epica = EpicaSerializer(read_only=True)
    epica_id = serializers.PrimaryKeyRelatedField(
        queryset=Epica.objects.all(), source="epica",
        write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = Tarea
        fields = (
            "id", "titulo", "descripcion", "criterios_aceptacion",
            "categoria", "estado", "completada", "fecha_cierre",
            "asignado_a", "asignado_a_id",
            "asignados", "asignados_ids",
            "sprint", "sprint_id",
            "epica", "epica_id",
        )

    def create(self, validated_data):
        asignados = validated_data.pop("asignados", [])
        obj = super().create(validated_data)
        if asignados:
            obj.asignados.set(asignados)
        return obj

    def update(self, instance, validated_data):
        asignados = validated_data.pop("asignados", None)
        obj = super().update(instance, validated_data)
        if asignados is not None:
            obj.asignados.set(asignados)
        return obj

class EvidenciaSerializer(serializers.ModelSerializer):
    creado_por = UserMiniSerializer(read_only=True)

    class Meta:
        model = Evidencia
        fields = ("id", "tarea", "comentario", "archivo", "creado_por", "creado_en", "actualizado_en")
        read_only_fields = ("tarea", "creado_por", "creado_en", "actualizado_en")
