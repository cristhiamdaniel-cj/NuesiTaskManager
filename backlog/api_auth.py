from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.middleware.csrf import get_token
import json

@require_GET
@ensure_csrf_cookie
def csrf_view(request):
    token = get_token(request)
    return JsonResponse({"detail": "CSRF cookie set", "csrfToken": token}, status=200)

@require_POST
@csrf_protect
def login_api(request):
    try:
        data = json.loads(request.body.decode() or "{}")
    except Exception:
        return JsonResponse({"detail": "JSON inválido"}, status=400)

    username = (data.get("username") or "").strip()
    password = data.get("password") or ""
    user = authenticate(request, username=username, password=password)

    if user is None:
        return JsonResponse({"detail": "Credenciales inválidas"}, status=401)

    login(request, user)
    must_change = user.check_password("neusi123")

    return JsonResponse({
        "id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "rol": getattr(getattr(user, "integrante", None), "rol", None),
        "is_authenticated": True,
        "must_change_password": must_change,
    }, status=200)

@require_GET
def me_api(request):
    u = request.user
    if not u.is_authenticated:
        return JsonResponse({"id": None, "is_authenticated": False}, status=200)
    return JsonResponse({
        "id": u.id,
        "username": u.username,
        "first_name": u.first_name,
        "rol": getattr(getattr(u, "integrante", None), "rol", None),
        "is_authenticated": True,
    }, status=200)

@require_POST
@csrf_protect
def logout_api(request):
    logout(request)
    return JsonResponse({"detail": "Sesión cerrada"}, status=200)
