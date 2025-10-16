from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsBacklogAdmin(BasePermission):
    def has_permission(self, request, view):
        integrante = getattr(request.user, "integrante", None)
        return bool(integrante and integrante.puede_crear_tareas())

class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        integrante = getattr(request.user, "integrante", None)
        if not integrante:
            return False
        if integrante.puede_crear_tareas():
            return True
        if request.method in SAFE_METHODS:
            return obj.asignado_a_id == getattr(integrante, "id", None)
        return obj.asignado_a_id == getattr(integrante, "id", None)
