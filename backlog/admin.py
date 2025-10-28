# backlog/admin.py
from django.contrib import admin
from django.utils import timezone
from datetime import datetime

from .models import (
    Integrante, Sprint, Epica, Tarea, Evidencia, Daily,
    Proyecto, PermisoProyecto
)

# ==========================
# Inline de permisos por proyecto
# ==========================
class PermisoProyectoInline(admin.TabularInline):
    model = PermisoProyecto
    extra = 1
    autocomplete_fields = ("proyecto",)
    fields = ("proyecto", "activo")
    verbose_name = "Proyecto autorizado"
    verbose_name_plural = "Proyectos autorizados (Visualizador / PO)"


# ==========================
# Integrante
# ==========================
@admin.register(Integrante)
class IntegranteAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "rol")
    search_fields = ("user__username", "user__first_name", "user__last_name", "rol")
    list_filter = ("rol",)
    ordering = ("user__username",)

    inlines = [PermisoProyectoInline]

    def get_inlines(self, request, obj=None):
        """
        Muestra el inline solo para roles Visualizador o Product Owner.
        """
        if not obj:
            return []
        roles_po = [getattr(Integrante, "ROL_PO", None), getattr(Integrante, "ROL_PO_COOFISAM", None)]
        roles_po = [r for r in roles_po if r]
        if obj.rol in [getattr(Integrante, "ROL_VISUALIZADOR", None), *roles_po]:
            return [PermisoProyectoInline]
        return []


# ==========================
# Sprint
# ==========================
@admin.register(Sprint)
class SprintAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "inicio", "fin")
    list_filter = ("inicio", "fin")
    search_fields = ("nombre",)
    ordering = ("-inicio",)


# ==========================
# Proyecto
# ==========================
@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nombre", "activo", "creado_en")
    list_filter = ("activo",)
    search_fields = ("codigo", "nombre")
    ordering = ("codigo",)


# ==========================
# Épica
# ==========================
@admin.register(Epica)
class EpicaAdmin(admin.ModelAdmin):
    list_display = ("codigo", "titulo", "proyecto", "estado", "prioridad", "progreso", "sprints_list", "creada_en")
    list_filter = ("proyecto", "estado", "prioridad")
    search_fields = ("codigo", "titulo", "descripcion", "kpis")
    autocomplete_fields = ("proyecto", "owner", "sprints")
    readonly_fields = ("progreso", "creada_en", "actualizada_en")
    ordering = ("-creada_en",)

    @admin.display(description="Avance (%)")
    def progreso(self, obj):
        try:
            return f"{obj.avance:.0f}%"
        except Exception:
            return "—"


# ==========================
# Tarea
# ==========================
@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = (
        "id", "titulo", "epica", "categoria", "estado",
        "asignado_a", "sprint", "completada", "fecha_cierre"
    )
    search_fields = ("titulo", "descripcion", "asignado_a__user__username", "epica__titulo")
    list_filter = ("categoria", "estado", "completada", "sprint", "epica")
    autocomplete_fields = ("asignado_a", "sprint", "epica")
    date_hierarchy = "fecha_cierre"
    ordering = ("-id",)
    readonly_fields = ("fecha_cierre",)

    fieldsets = (
        ("Información básica", {
            "fields": ("epica", "titulo", "descripcion", "criterios_aceptacion")
        }),
        ("Asignación", {
            "fields": ("categoria", "estado", "asignado_a", "sprint", "completada")
        }),
        ("Cierre", {
            "fields": ("informe_cierre", "fecha_cierre"),
            "classes": ("collapse",),
        }),
    )


# ==========================
# Evidencia
# ==========================
@admin.register(Evidencia)
class EvidenciaAdmin(admin.ModelAdmin):
    list_display = ("id", "tarea", "comentario_resumen", "creado_por", "creado_en")
    search_fields = ("tarea__titulo", "comentario", "creado_por__username")
    list_filter = ("creado_en",)
    autocomplete_fields = ("tarea", "creado_por")
    date_hierarchy = "creado_en"
    ordering = ("-creado_en",)

    def comentario_resumen(self, obj):
        if obj.comentario and len(obj.comentario) > 70:
            return obj.comentario[:70] + "…"
        return obj.comentario
    comentario_resumen.short_description = "Comentario"


# ==========================
# Daily
# ==========================
@admin.register(Daily)
class DailyAdmin(admin.ModelAdmin):
    list_display = ("id", "integrante", "fecha", "hora_local", "fuera_horario")
    search_fields = ("integrante__user__username", "integrante__user__first_name")
    list_filter = ("fuera_horario", "fecha")
    ordering = ("-fecha",)

    @admin.display(description="Hora (local)")
    def hora_local(self, obj):
        """
        Si guardas hora como TimeField + fecha aparte:
            mostramos tal cual, porque ya es hora local ingresada.
        Si en tu modelo 'hora' fuera DateTimeField:
            la convertimos a zona local con timezone.localtime().
        Así evitas ver 2pm cuando esperabas 7–9am.
        """
        h = getattr(obj, "hora", None)
        if h is None:
            return "—"

        # Caso 1: DateTimeField
        if hasattr(h, "tzinfo") or isinstance(h, datetime):
            try:
                return timezone.localtime(h).strftime("%H:%M")
            except Exception:
                return h.strftime("%H:%M")

        # Caso 2: TimeField (sin tz)
        try:
            return h.strftime("%H:%M")
        except Exception:
            return str(h)
