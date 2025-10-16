from django.contrib import admin
from .models import Sprint

@admin.register(Sprint)
class SprintAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "inicio", "fin")
    list_filter = ("inicio", "fin")
    search_fields = ("nombre",)

from .models import Integrante, Sprint, Epica, Tarea, Evidencia, Daily


# ==========================
# Integrante
# ==========================
@admin.register(Integrante)
class IntegranteAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "rol")
    search_fields = ("user__username", "user__first_name", "user__last_name", "rol")
    list_filter = ("rol",)
    ordering = ("user__username",)
