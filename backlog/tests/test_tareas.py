import pytest
from backlog.models import Proyecto, Epica, Sprint, Tarea, Integrante
from django.utils.timezone import now

@pytest.fixture
def tarea(db, user):
    integ = Integrante.objects.create(user=user, rol="MIEMBRO")
    proy = Proyecto.objects.create(codigo="PRJ1", nombre="Proyecto 1", activo=True)
    ep = Epica.objects.create(nombre="Épica Demo", proyecto=proy, owner=integ)
    sp = Sprint.objects.create(nombre="Sprint Demo", inicio=now().date(), fin=now().date())
    t = Tarea.objects.create(
        titulo="Tarea demo",
        epica=ep,
        sprint=sp,
        asignado_a=integ,
        categoria="UI",
        estado="PENDIENTE",
        completada=False,
    )
    return t

@pytest.mark.django_db
def test_patch_categoria_ok(auth_client, tarea):
    r = auth_client.patch(f"/api/backlog/tareas/{tarea.id}/categoria/", {"categoria": "NUI"}, format="json")
    assert r.status_code == 200
    assert r.data["ok"] is True
    assert r.data["data"]["categoria"] == "NUI"

@pytest.mark.django_db
def test_patch_categoria_invalida(auth_client, tarea):
    r = auth_client.patch(f"/api/backlog/tareas/{tarea.id}/categoria/", {"categoria": "XXX"}, format="json")
    assert r.status_code == 400
    assert r.data["ok"] is False

@pytest.mark.django_db
def test_patch_estado_completado(auth_client, tarea):
    r = auth_client.patch(f"/api/backlog/tareas/{tarea.id}/estado/", {"estado": "COMPLETADO"}, format="json")
    assert r.status_code == 200
    assert r.data["ok"] is True
    assert r.data["data"]["estado"] == "COMPLETADO"
