# NEUSI Task Manager – API de Autenticación (Backend)

**Desarrollado por:** Jorge Cardona
**Framework:** Django 5.2
**Puerto local:** 8076
=========================================================================

Base: /api/backlog/auth/
=========================================================================
1) Obtener CSRF

GET /csrf/

200 → setea cookie csrftoken (necesaria para POST/PATCH/DELETE).
=========================================================================
2) Login

POST /login/

Headers: Content-Type: application/json, X-CSRFToken: <csrftoken>

Body:

{ "username": "jorge", "password": "Jorge2025." }


200:

{
  "id": 4,
  "username": "jorge",
  "first_name": "",
  "rol": null,
  "is_authenticated": true,
  "must_change_password": false
}


Efecto: crea cookie sessionid y rota csrftoken.
=========================================================================
3) Usuario actual

GET /me/

200 autenticado:

{ "id": 4, "username": "jorge", "first_name": "", "rol": null, "is_authenticated": true }


200 sin sesión:

{ "id": null, "is_authenticated": false }
=========================================================================
4) Logout

POST /logout/

Headers: X-CSRFToken: <csrftoken actual>

200:

{ "detail": "Sesión cerrada" }
=========================================================================
Ejemplo (Next.js)
const API = '/api/backlog';

function getCookie(name: string) {
  return document.cookie.split('; ')
    .find(x => x.startsWith(name + '='))?.split('=')[1] ?? '';
}

export async function me() {
  const r = await fetch(`${API}/auth/me/`, { credentials: 'include' });
  return r.json();
}

export async function login(username: string, password: string) {
  await fetch(`${API}/auth/csrf/`, { credentials: 'include' });
  const csrftoken = getCookie('csrftoken');
  const r = await fetch(`${API}/auth/login/`, {
    method: 'POST',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrftoken },
    body: JSON.stringify({ username, password }),
  });
  if (!r.ok) throw new Error(`Login failed (${r.status})`);
  return r.json();
}

export async function logout() {
  const csrftoken = getCookie('csrftoken');
  const r = await fetch(`${API}/auth/logout/`, {
    method: 'POST',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrftoken },
    body: '{}',
  });
  return r.json();
}


---

**Autor**
Jorge Luis Cardona Gregory
Backend Developer – Octubre 2025
