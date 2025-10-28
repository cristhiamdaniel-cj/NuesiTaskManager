# disponibilidad/views.py
from datetime import datetime, timedelta
import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import DisponibilidadSemanal, HorarioDisponibilidad

# ⬅️ Ajusta si Integrante vive en otro app
from backlog.models import Integrante


# ============================
# Permisos (basado en Integrante)
# ============================
def _get_integrante(user):
    return getattr(user, "integrante", None)

def _es_admin(user):
    integ = _get_integrante(user)
    return bool((integ and integ.es_admin()) or getattr(user, "is_superuser", False))

def _es_visualizador(user):
    integ = _get_integrante(user)
    return bool(integ and integ.es_visualizador())


# ============================
# Semana utilidades
# ============================
def _lunes_de(fecha):
    """Devuelve el lunes de la semana de `fecha`."""
    return fecha - timedelta(days=fecha.weekday())

def _get_semana_inicio(request):
    """
    Usa ?semana=YYYY-MM-DD (cualquier día) y lo normaliza a lunes.
    Si no viene, usa la semana actual según el modelo.
    """
    raw = request.GET.get("semana")
    if raw:
        try:
            dt = datetime.strptime(raw, "%Y-%m-%d").date()
            return _lunes_de(dt)
        except ValueError:
            pass
    return DisponibilidadSemanal.obtener_semana_actual()

def _prev_next(semana_inicio):
    return semana_inicio - timedelta(days=7), semana_inicio + timedelta(days=7)


# ============================
# Vista: Mi disponibilidad (grilla 7x24)
# ============================
@login_required
def mi_disponibilidad(request):
    semana_inicio = _get_semana_inicio(request)

    # ¿puede editar?
    puede_editar, mensaje_edicion = DisponibilidadSemanal.puede_editar_usuario(request.user)

    # Obtener/crear cabecera semanal
    disp_sem, _ = DisponibilidadSemanal.objects.get_or_create(
        usuario=request.user,
        semana_inicio=semana_inicio,
        defaults={"actualizado_por": request.user},
    )

    # Traer TODOS los horarios de esta semana en una sola query
    horarios = (
        HorarioDisponibilidad.objects
        .filter(disponibilidad_semanal=disp_sem)
        .values("dia_semana", "hora", "estado", "notas", "id")
    )

    # Construir matriz 7x24 (diccionario de diccionarios)
    matriz = {d: {h: None for h in range(24)} for d in range(7)}
    for h in horarios:
        matriz[h["dia_semana"]][h["hora"]] = h  # puedes acceder estado/id en el template

    prev_w, next_w = _prev_next(semana_inicio)

    context = {
        "disponibilidad": disp_sem,
        "horarios_matriz": matriz,
        "puede_editar": puede_editar,
        "mensaje_edicion": mensaje_edicion,
        "dias_semana": HorarioDisponibilidad.DIAS_SEMANA,
        "horas": range(24),
        "estados": HorarioDisponibilidad.ESTADOS_DISPONIBILIDAD,

        # navegación superior
        "semana_inicio": semana_inicio,
        "prev_w": prev_w,
        "next_w": next_w,
        "home_url": "/",
        "equipo_url": reverse("disponibilidad:equipo_disponibilidad") + f"?semana={semana_inicio.isoformat()}",
        "puede_ver_equipo": _es_admin(request.user) or _es_visualizador(request.user),
    }
    return render(request, "disponibilidad/mi_disponibilidad.html", context)


# ============================
# AJAX: actualizar una celda (hora)
# ============================
@login_required
@require_POST
def actualizar_horario(request):
    """
    JSON esperado:
    {
      "dia_semana": 0..6,
      "hora": 0..23,
      "estado": "disponible" | "ocupado" | "parcial",
      "semana": "YYYY-MM-DD"   # opcional; cualquier fecha de la semana
    }
    """
    try:
        data = json.loads(request.body or "{}")
        dia_semana = int(data.get("dia_semana"))
        hora = int(data.get("hora"))
        nuevo_estado = data.get("estado")
        semana_raw = data.get("semana")  # opcional

        # Validaciones básicas
        if dia_semana < 0 or dia_semana > 6 or hora < 0 or hora > 23:
            return JsonResponse({"success": False, "error": "Parámetros fuera de rango."}, status=400)

        estados_validos = {e[0] for e in HorarioDisponibilidad.ESTADOS_DISPONIBILIDAD}
        if nuevo_estado not in estados_validos:
            return JsonResponse({"success": False, "error": "Estado no válido."}, status=400)

        # ¿Puede editar?
        puede_editar, msg = DisponibilidadSemanal.puede_editar_usuario(request.user)
        if not puede_editar:
            return JsonResponse({"success": False, "error": msg}, status=403)

        # Determinar semana
        if semana_raw:
            try:
                fecha = datetime.strptime(semana_raw, "%Y-%m-%d").date()
                semana_inicio = _lunes_de(fecha)
            except ValueError:
                return JsonResponse({"success": False, "error": "Semana inválida."}, status=400)
        else:
            semana_inicio = DisponibilidadSemanal.obtener_semana_actual()

        # Cabecera semanal del usuario
        disp_sem, _ = DisponibilidadSemanal.objects.get_or_create(
            usuario=request.user,
            semana_inicio=semana_inicio,
            defaults={"actualizado_por": request.user},
        )

        # Guardar/crear la celda
        HorarioDisponibilidad.objects.update_or_create(
            disponibilidad_semanal=disp_sem,
            dia_semana=dia_semana,
            hora=hora,
            defaults={
                "estado": nuevo_estado,
                "notas": "",
            },
        )

        # Marcar quién actualizó
        disp_sem.actualizado_por = request.user
        disp_sem.save(update_fields=["actualizado_por", "actualizado_en"])

        return JsonResponse({"success": True, "mensaje": "Horario actualizado correctamente."})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


# ============================
# Vista: Equipo (admin/visualizador)
# ============================
@login_required
def ver_disponibilidad_equipo(request):
    if not (_es_admin(request.user) or _es_visualizador(request.user)):
        return HttpResponseForbidden("Solo administradores/visualizadores.")

    semana_inicio = _get_semana_inicio(request)
    prev_w, next_w = _prev_next(semana_inicio)

    # Filtros
    grupo_id = request.GET.get("grupo")
    usuario_id = request.GET.get("usuario")

    usuarios = User.objects.all().order_by("first_name", "last_name")
    if grupo_id:
        try:
            g = Group.objects.get(pk=int(grupo_id))
            usuarios = usuarios.filter(groups=g)
        except (ValueError, Group.DoesNotExist):
            messages.error(request, "Grupo inválido.")

    if usuario_id:
        try:
            usuarios = usuarios.filter(id=int(usuario_id))
        except (ValueError, User.DoesNotExist):
            messages.error(request, "Usuario inválido.")

    # Construir filas: por usuario traemos su cabecera semanal y su matriz 7x24
    rows = []
    for u in usuarios:
        disp_sem, _ = DisponibilidadSemanal.objects.get_or_create(
            usuario=u,
            semana_inicio=semana_inicio,
            defaults={"actualizado_por": request.user},  # quien lo crea por primera vez
        )

        # Traer en bloque los horarios de ese usuario/semana
        horarios = (
            HorarioDisponibilidad.objects
            .filter(disponibilidad_semanal=disp_sem)
            .values("dia_semana", "hora", "estado", "id")
        )

        matriz = {d: {h: None for h in range(24)} for d in range(7)}
        for h in horarios:
            matriz[h["dia_semana"]][h["hora"]] = h

        rows.append({"user": u, "sem": disp_sem, "matriz": matriz})

    context = {
        "rows": rows,
        "semana_inicio": semana_inicio,
        "prev_w": prev_w,
        "next_w": next_w,

        # combos y filtros
        "grupos": Group.objects.all().order_by("name"),
        "grupo_sel": grupo_id,
        "todos_usuarios": User.objects.all().order_by("first_name", "last_name"),
        "usuario_sel": usuario_id,

        # navegación
        "home_url": "/",
        "mi_url": reverse("disponibilidad:mi_disponibilidad") + f"?semana={semana_inicio.isoformat()}",
    }
    return render(request, "disponibilidad/equipo_disponibilidad.html", context)
