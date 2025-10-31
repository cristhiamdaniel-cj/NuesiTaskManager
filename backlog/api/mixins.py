# backlog/api/mixins.py
from rest_framework.response import Response

class EnvelopeMixin:
    """
    Envueltas estándar en { ok, data, meta } para respuestas 2xx.
    Úsalo junto a ModelViewSet/ReadOnlyModelViewSet.
    """
    def _ok(self, data=None, meta=None, status=200):
        return Response({"ok": True, "data": data, "meta": meta}, status=status)

    # list/retrieve
    def list(self, request, *args, **kwargs):
        resp = super().list(request, *args, **kwargs)
        return self._ok(resp.data)

    def retrieve(self, request, *args, **kwargs):
        resp = super().retrieve(request, *args, **kwargs)
        return self._ok(resp.data)

    # create/update/partial_update/destroy
    def create(self, request, *args, **kwargs):
        resp = super().create(request, *args, **kwargs)
        return self._ok(resp.data, status=201)

    def update(self, request, *args, **kwargs):
        resp = super().update(request, *args, **kwargs)
        return self._ok(resp.data)

    def partial_update(self, request, *args, **kwargs):
        resp = super().partial_update(request, *args, **kwargs)
        return self._ok(resp.data)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return self._ok(None, status=204)
