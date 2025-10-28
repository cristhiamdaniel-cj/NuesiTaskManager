from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsBacklogAdmin(BasePermission):
    """Permite todo a quien sea admin del backlog (rol en Integrante)."""
    def has_permission(self, request, view):
        integrante = getattr(request.user, "integrante", None)
        return bool(integrante and integrante.puede_crear_tareas())

class IsOwnerOrAdmin(BasePermission):
    """
    Permite acceso si:
      - es admin backlog, o
      - es responsable de la tarea (FK asignado_a o M2M asignados).
    Lecturas (SAFE_METHODS) también restringidas al mismo criterio.
    """
    def has_object_permission(self, request, view, obj):
        integrante = getattr(request.user, "integrante", None)
        if not integrante:
            return False
        if integrante.puede_crear_tareas():
            return True
        is_resp = (
            obj.asignado_a_id == getattr(integrante, "id", None)
            or obj.asignados.filter(id=integrante.id).exists()
        )
        if request.method in SAFE_METHODS:
            return is_resp
        return is_resp
