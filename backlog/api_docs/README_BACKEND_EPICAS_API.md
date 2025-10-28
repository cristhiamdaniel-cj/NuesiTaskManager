NEUSI Task Manager – API de Épicas (Backend)

Módulo: Gestión de Épicas
Framework: Django 5.2
Ruta base: /api/backlog/epicas/
Versión: Octubre 2025
Desarrollado por: Jorge Cardona
=========================================================================
Descripción general

Las épicas representan los objetivos estratégicos o líneas de trabajo principales del backlog.
Cada sprint y tarea puede vincularse a una épica, lo que facilita agrupar y medir avances por meta o producto.
=========================================================================
Endpoints principales
1️⃣ Crear épica

POST /api/backlog/epicas/
Headers:

Content-Type: application/json
X-CSRFToken: <valor de la cookie csrftoken>


Body:

{
  "nombre": "Épica - Backlog NEUSI",
  "descripcion": "Organización general del producto",
  "prioridad": 2,
  "owner_id": 3,
  "proyecto_id": 1
}


Respuesta 201:

{
  "id": 7,
  "nombre": "Épica - Backlog NEUSI",
  "descripcion": "Organización general del producto",
  "prioridad": 2,
  "activa": true,
  "owner": { "id": 3, "username": "jorge" },
  "proyecto": { "id": 1, "codigo": "P001", "nombre": "NEUSI" },
  "creada_en": "2025-10-28T15:34:10Z"
}
=========================================================================
2️⃣ Listar épicas

GET /api/backlog/epicas/

Respuesta 200:

[
  {
    "id": 7,
    "nombre": "Épica - Backlog NEUSI",
    "descripcion": "Organización general del producto",
    "prioridad": 2,
    "activa": true,
    "owner": { "id": 3, "username": "jorge" },
    "proyecto": { "id": 1, "nombre": "NEUSI" },
    "creada_en": "2025-10-28T15:34:10Z"
  }
]
=========================================================================
3️⃣ Actualizar parcialmente (PATCH)

PATCH /api/backlog/epicas/{id}/
Body:

{ "nombre": "Épica - Revisión Final" }


Respuesta 200:

{ "id": 7, "nombre": "Épica - Revisión Final", "prioridad": 2 }
=========================================================================
4️⃣ Asignar responsable (owner)

PATCH /api/backlog/epicas/{id}/
Body:

{ "owner_id": 1 }


Efecto: Actualiza el usuario responsable (Integrante) de la épica.
=========================================================================
5️⃣ Reemplazo total (PUT)

PUT /api/backlog/epicas/{id}/
Body:

{
  "nombre": "Épica - Revisión Final",
  "descripcion": "Edición completa vía PUT",
  "prioridad": 3,
  "activa": true,
  "owner_id": 1,
  "proyecto_id": 2
}


Respuesta 200:

{
  "id": 7,
  "nombre": "Épica - Revisión Final",
  "descripcion": "Edición completa vía PUT",
  "prioridad": 3,
  "activa": true,
  "owner": { "id": 1, "username": "admin" },
  "proyecto": { "id": 2, "nombre": "Sprint Planning" }
}
=========================================================================
6️⃣ Eliminar épica

DELETE /api/backlog/epicas/{id}/

Respuesta 204: (sin contenido)
=========================================================================
Reglas para el Frontend

Requiere autenticación y cabecera X-CSRFToken.
Campo owner_id debe provenir de /api/backlog/integrantes/.
Campo proyecto_id opcional, tomado de /api/backlog/proyectos/ (si aplica).
Ideal representar en UI como tarjetas ("Epic Cards") con nombre, prioridad y responsable.
Solo usuarios con permisos Backlog Admin pueden crear o editar épicas.
=========================================================================
Estado del módulo
Funcionalidad	Estado Backend
Crear	✅ OK
Listar	✅ OK
Editar / PATCH	✅ OK
Asignar owner	✅ OK
Eliminar	✅ OK
Integración CSRF	✅ OK
=========================================================================
Autor: Jorge Luis Cardona Gregory
Rol: Backend Developer
Fecha: Octubre 2025