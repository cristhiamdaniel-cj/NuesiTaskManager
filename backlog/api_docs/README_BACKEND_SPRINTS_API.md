NEUSI Task Manager – API de Sprints (Backend)

Módulo: Gestión de Sprints
Framework: Django 5.2
Ruta base: /api/backlog/sprints/
Versión: Octubre 2025
Desarrollado por: Jorge Cardona
=========================================================================
Descripción general

Los sprints representan los ciclos de trabajo del backlog.
Cada sprint agrupa tareas y épicas, definiendo fechas de inicio y fin.
=========================================================================
Endpoints principales
1️⃣ Crear sprint

POST /api/backlog/sprints/
Headers:

Content-Type: application/json
X-CSRFToken: <valor de la cookie csrftoken>


Body:

{
  "nombre": "Sprint 10 - Octubre",
  "inicio": "2025-10-28",
  "fin": "2025-11-08",
  "objetivo": "Pruebas de integración backlog + matriz"
}


Respuesta 201:

{
  "id": 5,
  "nombre": "Sprint 10 - Octubre",
  "inicio": "2025-10-28",
  "fin": "2025-11-08",
  "objetivo": "Pruebas de integración backlog + matriz"
}
=========================================================================
2️⃣ Listar sprints

GET /api/backlog/sprints/

[
  { "id": 1, "nombre": "Sprint 9", "inicio": "2025-10-10", "fin": "2025-10-20" },
  { "id": 2, "nombre": "Sprint 10", "inicio": "2025-10-28", "fin": "2025-11-08" }
]
=========================================================================
3️⃣ Actualizar (PATCH)

PATCH /api/backlog/sprints/{id}/

{ "objetivo": "Revisión de backlog y testing final" }


Respuesta 200:

{ "id": 5, "nombre": "Sprint 10 - Octubre", "objetivo": "Revisión de backlog y testing final" }
=========================================================================
4️⃣ Reemplazar completamente (PUT)

PUT /api/backlog/sprints/{id}/

{
  "nombre": "Sprint Final",
  "inicio": "2025-11-10",
  "fin": "2025-11-25",
  "objetivo": "Entrega final del sistema"
}
=========================================================================
5️⃣ Eliminar sprint

DELETE /api/backlog/sprints/{id}/
Respuesta 204: (sin contenido)
=========================================================================
Reglas para el Frontend

Debe mostrarse como lista o calendario con rango de fechas.
Asociar tareas y épicas por sprint_id.
Solo usuarios con permisos Backlog Admin pueden crear o editar.
Usa siempre credentials: "include" y X-CSRFToken.
=========================================================================
Estado del módulo
Funcionalidad	Estado
Crear	✅ OK
Listar	✅ OK
Editar / PATCH	✅ OK
Eliminar	✅ OK
CSRF y sesión	✅ OK
=========================================================================
Autor: Jorge Luis Cardona Gregory
Rol: Backend Developer
Fecha: Octubre 2025