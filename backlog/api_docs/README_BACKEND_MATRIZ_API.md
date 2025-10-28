NEUSI Task Manager – API de Matriz Eisenhower

Módulo: Matriz de Prioridades
Framework: Django 5.2
Ruta base: /api/backlog/matriz/
Versión: Octubre 2025
Desarrollado por: Jorge Cardona
=========================================================================
Descripción general

La matriz Eisenhower permite visualizar las tareas clasificadas según urgencia e importancia:
=========================================================================
Categoría	Significado
UI	Urgente e Importante
NUI	No Urgente e Importante
UNI	Urgente y No Importante
NUNI	No Urgente y No Importante
=========================================================================
Endpoint principal

GET /api/backlog/matriz/
Respuesta:

{
  "ui": [
    { "id": 12, "titulo": "Resolver bug crítico", "categoria": "UI" }
  ],
  "nui": [
    { "id": 14, "titulo": "Documentar backlog", "categoria": "NUI" }
  ],
  "uni": [],
  "nuni": []
}
=========================================================================
Parámetros opcionales
| Parámetro | Descripción                         |
| --------- | ----------------------------------- |
| `persona` | Filtra por integrante               |
| `sprint`  | Filtra por sprint                   |
| `epica`   | Filtra por épica                    |
| `mine=1`  | Solo tareas del usuario autenticado |

=========================================================================
Reglas para el Frontend

Requiere autenticación (credentials: include).

=========================================================================
Mostrar cada cuadrante con color:

🔴 UI, 🟢 NUI, 🟡 UNI, ⚫ NUNI.

Ideal para tablero visual tipo “drag & drop” (opcional).

Lectura simple: solo GET, sin modificaciones.

=========================================================================
Estado del módulo
Funcionalidad	Estado
Listado por cuadrantes	✅ OK
Filtros integrados	✅ OK
CSRF y sesión	✅ OK

=========================================================================
Autor: Jorge Luis Cardona Gregory
Rol: Backend Developer
Fecha: Octubre 2025