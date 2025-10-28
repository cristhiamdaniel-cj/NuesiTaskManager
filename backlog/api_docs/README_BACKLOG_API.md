README_BACKLOG_API.md
NEUSI Task Manager – Backlog API (Índice general)
=========================================================================
Framework: Django 5.2 + DRF
Base local: http://localhost:8076/api/backlog/
Prod/ngrok: https://devops-neusi.ngrok.io/api/backlog/
=========================================================================
Módulos y docs

| Módulo        | Archivo                         Descripción                                            |
| ------------- | ------------------------------- ------------------------------------------------------ |
| Autenticación | `README_AUTH_BACKEND_LOGIN.md`  |CSRF, login, me, ogout                                |
| Épicas        | `README_BACKEND_EPICAS_API.md`  |CRUD yasignación de owner/Proyecto                    |
| Sprints       | `README_BACKEND_SPRINTS_API.md` |CRUD de Prints                                        |
| Tareas        | `README_BACKEND_TAREAS_API.md`  |CRUD, filtros, acciones (estado/categoría)evidencias |
| Matriz        | `README_BACKEND_MATRIZ_API.md`  |Cuadrante UI/NUI/UNI/NUNI XFiltros                  |

=========================================================================
Rutas registradas (DRF Router)
/api/backlog/integrantes/
/api/backlog/epicas/
/api/backlog/sprints/
/api/backlog/tareas/
/api/backlog/matriz/          # vista de colección
/api/backlog/auth/**          # ver doc de auth
=========================================================================
Reglas universales (Frontend)

Siempre credentials: 'include' en fetch.
Antes de cualquier POST/PATCH/DELETE: GET /api/backlog/auth/csrf/.
Incluir X-CSRFToken (valor de cookie csrftoken) en métodos que mutan datos.
Si GET /auth/me/ no retorna JSON o viene 403 → sesión expirada (pedir login).
=========================================================================