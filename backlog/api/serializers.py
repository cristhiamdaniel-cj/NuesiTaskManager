from rest_framework import serializers
from django.contrib.auth.models import User
from ..models import Integrante, Epica, Sprint, Tarea, Evidencia, Daily

class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id","username","first_name","last_name","email")

class IntegranteSerializer(serializers.ModelSerializer):
    user = UserMiniSerializer()
    class Meta:
        model = Integrante
        fields = ("id","rol","user")

class EpicaSerializer(serializers.ModelSerializer):
    owner = IntegranteSerializer(read_only=True)
    owner_id = serializers.PrimaryKeyRelatedField(queryset=Integrante.objects.all(), source="owner", write_only=True, required=False, allow_null=True)
    class Meta:
        model = Epica
        fields = ("id","nombre","descripcion","owner","owner_id","prioridad","activa","creada_en")

class SprintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sprint
        fields = ("id","nombre","inicio","fin")

class TareaSerializer(serializers.ModelSerializer):
    asignado_a = IntegranteSerializer(read_only=True)
    asignado_a_id = serializers.PrimaryKeyRelatedField(queryset=Integrante.objects.all(), source="asignado_a", write_only=True, required=False, allow_null=True)
    sprint = SprintSerializer(read_only=True)
    sprint_id = serializers.PrimaryKeyRelatedField(queryset=Sprint.objects.all(), source="sprint", write_only=True)
    epica = EpicaSerializer(read_only=True)
    epica_id = serializers.PrimaryKeyRelatedField(queryset=Epica.objects.all(), source="epica", write_only=True, required=False, allow_null=True)

    class Meta:
        model = Tarea
        fields = ("id","titulo","descripcion","criterios_aceptacion","categoria","estado","completada","fecha_cierre",
                  "asignado_a","asignado_a_id","sprint","sprint_id","epica","epica_id")

class EvidenciaSerializer(serializers.ModelSerializer):
    creado_por = UserMiniSerializer(read_only=True)
    class Meta:
        model = Evidencia
        fields = ("id","tarea","comentario","archivo","creado_por","creado_en","actualizado_en")
        read_only_fields = ("tarea","creado_por","creado_en","actualizado_en")

class DailySerializer(serializers.ModelSerializer):
    integrante = IntegranteSerializer(read_only=True)
    integrante_id = serializers.PrimaryKeyRelatedField(queryset=Integrante.objects.all(), source="integrante", write_only=True)
    class Meta:
        model = Daily
        fields = ("id","integrante","integrante_id","fecha","hora","que_hizo_ayer","que_hara_hoy","impedimentos","fuera_horario")
