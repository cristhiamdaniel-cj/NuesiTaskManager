NEUSI Task Manager – API de Tareas (Backend)
=========================================================================
Módulo: Gestión de Tareas
Framework: Django 5.2
Ruta base: /api/backlog/tareas/
Versión: Octubre 2025
Desarrollado por: Jorge Cardona
=========================================================================
Descripción general

Las tareas son las unidades mínimas de trabajo del backlog.
Cada tarea puede pertenecer a un sprint, épica o proyecto, y tener varios asignados.
=========================================================================
Endpoints principales
1️⃣ Crear tarea

POST /api/backlog/tareas/

{
  "titulo": "Integrar vista Kanban",
  "descripcion": "Diseñar la interfaz y lógica drag & drop",
  "categoria": "UI",
  "sprint_id": 5,
  "epica_id": 7,
  "asignado_a": 3
}
=========================================================================
2️⃣ Listar tareas (con filtros opcionales)

GET /api/backlog/tareas/?persona=3&sprint=5&estado=abiertas

[
  {
    "id": 10,
    "titulo": "Integrar vista Kanban",
    "categoria": "UI",
    "epica": "Backlog NEUSI",
    "sprint": "Sprint 10",
    "asignado_a": "jorge",
    "completada": false
  }
]
=========================================================================
3️⃣ Actualizar parcialmente (PATCH)

PATCH /api/backlog/tareas/{id}/

{ "titulo": "Integrar matriz Eisenhower" }
=========================================================================
4️⃣ Cambiar categoría

PATCH /api/backlog/tareas/{id}/categoria/

{ "categoria": "NUI" }
=========================================================================
5️⃣ Cambiar estado

PATCH /api/backlog/tareas/{id}/estado/

{ "estado": "COMPLETADO" }


Efecto: Marca la tarea como completada y registra la fecha de cierre.
=========================================================================
6️⃣ Crear evidencia

POST /api/backlog/tareas/{id}/evidencias/

{ "descripcion": "Informe final de validación" }
=========================================================================
7️⃣ Eliminar tarea

DELETE /api/backlog/tareas/{id}/
Respuesta: 204 No Content

Filtros disponibles
Parámetro	Descripción
persona	ID del integrante asignado
sprint	ID del sprint
epica	ID de la épica
estado	abiertas o cerradas
mine=1	Muestra solo las tareas del usuario actual
Reglas para el Frontend

Requiere login (CSRF + sessionid).
=========================================================================
Mostrar badges según categoria:

🔴 UI, 🟢 NUI, 🟡 UNI, ⚫ NUNI.

Los campos estado y categoria se actualizan con acciones PATCH.

Asociar evidencias como anexos o comentarios visuales.
=========================================================================
Estado del módulo
Funcionalidad	Estado
CRUD completo	✅ OK
Filtros	✅ OK
Acciones PATCH	✅ OK
Evidencias	✅ OK
=========================================================================
Autor: Jorge Luis Cardona Gregory
Rol: Backend Developer
Fecha: Octubre 2025