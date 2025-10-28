# apps/backlog/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError

# ==============================
# Validadores
# ==============================
def validar_story_points(value):
    """Fibonacci corta; permite nulo."""
    if value is None:
        return
    validos = (1, 2, 3, 5, 8, 13, 21)
    if value not in validos:
        raise ValidationError(f"Los story points deben ser uno de: {', '.join(map(str, validos))}.")

# ==============================
# Integrante
# ==============================
class Integrante(models.Model):
    """Perfil 1:1 con User. Los permisos se derivan del campo 'rol'."""

    # Roles canónicos
    ROL_SM_PO       = "Scrum Master / PO"
    ROL_ARQ_DIR     = "Arquitecto de Software y Director General"
    ROL_GH          = "Coordinadora de Gestión Humana y Administrativa"

    # Visualizadores / dueños de producto (solo lectura app)
    ROL_VISUALIZADOR = "Visualizador"
    ROL_PO           = "Product Owner"
    ROL_PO_COOFISAM  = "Product Owner Coofisam360"

    # Otros roles operativos (solo lectura por defecto; permisos dados por views)
    ROL_DBA            = "Administrador de Bases de Datos (DBA)"
    ROL_LIDER_COMERCIAL= "Líder Comercial"
    ROL_BI             = "Especialista en Visualización y BI"
    ROL_DEV_FE         = "Desarrollador Frontend"
    ROL_DEV_BE         = "Desarrollador Backend"
    ROL_MKT            = "Coordinadora de Marketing y Comunicación"
    ROL_CONTABLE       = "Contadora General"
    ROL_MIEMBRO        = "Miembro"

    ROL_CHOICES = [
        (ROL_SM_PO, ROL_SM_PO),
        (ROL_ARQ_DIR, ROL_ARQ_DIR),
        (ROL_GH, ROL_GH),

        (ROL_VISUALIZADOR, ROL_VISUALIZADOR),
        (ROL_PO, ROL_PO),
        (ROL_PO_COOFISAM, ROL_PO_COOFISAM),

        (ROL_DBA, ROL_DBA),
        (ROL_LIDER_COMERCIAL, ROL_LIDER_COMERCIAL),
        (ROL_BI, ROL_BI),
        (ROL_DEV_FE, ROL_DEV_FE),
        (ROL_DEV_BE, ROL_DEV_BE),
        (ROL_MKT, ROL_MKT),
        (ROL_CONTABLE, ROL_CONTABLE),
        (ROL_MIEMBRO, ROL_MIEMBRO),
    ]

    # Matriz de permisos por rol (puedes ajustar en el tiempo)
    ROL_PERMISOS = {
        ROL_SM_PO: {"crear_tareas", "agregar_evidencias", "editar_tareas"},
        ROL_ARQ_DIR: {"crear_tareas", "agregar_evidencias", "editar_tareas"},
        ROL_GH: {"crear_tareas", "agregar_evidencias", "editar_tareas"},
        # resto lectura por defecto
    }

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="integrante")
    rol  = models.CharField(max_length=100, choices=ROL_CHOICES, default=ROL_MIEMBRO)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

    # ===== Helpers de rol/permisos =====
    def _perms(self):
        return self.ROL_PERMISOS.get(self.rol, set())

    def es_visualizador(self) -> bool:
        return self.rol in {self.ROL_VISUALIZADOR, self.ROL_PO, self.ROL_PO_COOFISAM}

    def es_admin(self) -> bool:
        return self.rol in {self.ROL_SM_PO, self.ROL_ARQ_DIR, self.ROL_GH} or getattr(self.user, "is_superuser", False)

    def puede_crear_tareas(self) -> bool:
        return "crear_tareas" in self._perms() or self.es_admin()

    def puede_agregar_evidencias(self) -> bool:
        return "agregar_evidencias" in self._perms() or self.es_admin()

    def puede_editar_tareas(self) -> bool:
        return "editar_tareas" in self._perms() or self.es_admin()

# ==============================
# Proyecto (normalizado)
# ==============================
class Proyecto(models.Model):
    codigo = models.CharField(max_length=30, unique=True,
                              help_text="Identificador corto (ej. NEUCONTA, CPS, JURIDICO).")
    nombre = models.CharField(max_length=150)
    activo = models.BooleanField(default=True)

    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["codigo"]

    def __str__(self):
        return f"{self.codigo} — {self.nombre}"

# ==============================
# Permisos de Proyecto (para visualizadores/PO)
# ==============================
class PermisoProyecto(models.Model):
    integrante = models.ForeignKey("Integrante", on_delete=models.CASCADE, related_name="permisos_proyectos")
    proyecto   = models.ForeignKey("Proyecto", on_delete=models.CASCADE, related_name="permisos_integrantes")
    activo     = models.BooleanField(default=True)
    creado_en  = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        unique_together = ("integrante", "proyecto")

    def __str__(self):
        estado = "Activo" if self.activo else "Inactivo"
        return f"{self.integrante} → {self.proyecto} ({estado})"

# ==============================
# Sprint
# ==============================
class Sprint(models.Model):
    nombre = models.CharField(max_length=50, default="Sprint")
    inicio = models.DateField()
    fin    = models.DateField()

    def __str__(self):
        return f"{self.nombre} ({self.inicio} - {self.fin})"

# ==============================
# Épica
# ==============================
class Epica(models.Model):
    ESTADO_CHOICES = [
        ("PROPUESTA", "Propuesta"),
        ("ACTIVA", "Activa"),
        ("EN_PAUSA", "En pausa"),
        ("CERRADA", "Cerrada"),
    ]
    PRIORIDAD_CHOICES = [("ALTA", "Alta"), ("MEDIA", "Media"), ("BAJA", "Baja")]

    codigo = models.CharField(max_length=20, unique=True, null=True, blank=True,
                              help_text="Código legible (ej. NEUSI-001).")
    titulo = models.CharField(max_length=200, unique=True)
    descripcion = models.TextField(blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default="ACTIVA")
    prioridad = models.CharField(max_length=10, choices=PRIORIDAD_CHOICES, default="MEDIA")

    proyecto = models.ForeignKey("Proyecto", on_delete=models.PROTECT, null=True, blank=True,
                                 related_name="epicas", help_text="Proyecto al que pertenece esta épica.")

    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin    = models.DateField(null=True, blank=True)

    kpis = models.TextField(blank=True, help_text="Métricas clave esperadas para la épica")

    # Avance manual 0–100; si None se calcula por tareas
    avance_manual = models.PositiveSmallIntegerField(null=True, blank=True,
                                                    help_text="0–100. Si se deja vacío, se calcula por tareas.")

    # Responsable legacy + múltiples responsables
    owner  = models.ForeignKey("Integrante", on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="epicas_propias")
    owners = models.ManyToManyField("Integrante", blank=True, related_name="epicas_cocreadas",
                                    help_text="Responsables/co-owners de la épica")

    sprints = models.ManyToManyField("Sprint", blank=True, related_name="epicas")

    documentos_url = models.URLField(blank=True, help_text="Enlace a carpeta o documento maestro")

    creada_en = models.DateTimeField(auto_now_add=True)
    actualizada_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-creada_en"]

    def __str__(self):
        pref = f"{self.codigo} - " if self.codigo else ""
        return f"{pref}{self.titulo}"

    # ===== Métricas =====
    @property
    def total_tareas(self) -> int:
        return self.tareas.count()

    @property
    def tareas_completadas(self) -> int:
        return self.tareas.filter(completada=True).count()

    @property
    def progreso_calculado(self) -> float:
        total = self.total_tareas
        return round((self.tareas_completadas / total) * 100.0, 2) if total else 0.0

    @property
    def avance(self) -> float:
        return float(self.avance_manual) if self.avance_manual is not None else self.progreso_calculado

    def sprints_list(self):
        return ", ".join(str(s) for s in self.sprints.all())
    sprints_list.short_description = "Sprints"

    def clean(self):
        if self.fecha_inicio and self.fecha_fin and self.fecha_inicio > self.fecha_fin:
            raise ValidationError("La fecha de inicio no puede ser posterior a la fecha fin.")
        if self.avance_manual is not None and not (0 <= self.avance_manual <= 100):
            raise ValidationError("El avance manual debe estar entre 0 y 100.")

# ==============================
# Tarea
# ==============================
class Tarea(models.Model):
    MATRIZ_CHOICES = [
        ("UI", "Urgente e Importante"),
        ("NUI", "No Urgente e Importante"),
        ("UNI", "Urgente y No Importante"),
        ("NUNI", "No Urgente y No Importante"),
    ]
    ESTADO_CHOICES = [
        ("NUEVO", "Nuevo"),
        ("APROBADO", "Aprobado"),
        ("EN_PROGRESO", "En Progreso"),
        ("COMPLETADO", "Completado"),
        ("BLOQUEADO", "Bloqueado"),
    ]

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    criterios_aceptacion = models.TextField(blank=True, help_text="Criterios para cerrar la tarea")
    categoria = models.CharField(max_length=4, choices=MATRIZ_CHOICES)

    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default="NUEVO",
                              help_text="Estado actual en el workflow")

    # Story points (Fibonacci)
    esfuerzo_sp = models.PositiveSmallIntegerField(null=True, blank=True,
                                                   validators=[validar_story_points],
                                                   help_text="Story points (1, 2, 3, 5, 8, 13, 21)")

    epica = models.ForeignKey("Epica", on_delete=models.SET_NULL, null=True, blank=True, related_name="tareas")

    # Múltiples responsables (nuevo)
    asignados = models.ManyToManyField("Integrante", blank=True, related_name="tareas_asignadas")

    # Responsable único (legado/compatibilidad)
    asignado_a = models.ForeignKey("Integrante", on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name="tareas_asignadas_legacy")

    sprint = models.ForeignKey("Sprint", on_delete=models.CASCADE)

    completada   = models.BooleanField(default=False)
    fecha_cierre = models.DateTimeField(null=True, blank=True)
    informe_cierre = models.FileField(upload_to="informes_cierre/", blank=True, null=True,
                                      help_text="Archivo requerido para cerrar la tarea")

    def __str__(self):
        return f"{self.titulo} ({self.get_categoria_display()})"

    @property
    def esfuerzo_display(self):
        return self.esfuerzo_sp if self.esfuerzo_sp is not None else "-"

    @property
    def responsables_list(self):
        nombres = [str(i) for i in self.asignados.all()]
        return ", ".join(nombres) if nombres else "—"

# ==============================
# Evidencia
# ==============================
class Evidencia(models.Model):
    tarea = models.ForeignKey("Tarea", on_delete=models.CASCADE, related_name="evidencias")
    comentario = models.TextField(blank=True, null=True)
    archivo = models.FileField(upload_to="evidencias/", blank=True, null=True)

    creado_por = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    creado_en = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    actualizado_en = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"Evidencia de {self.tarea.titulo} ({self.creado_por})"

# ==============================
# Daily
# ==============================
class Daily(models.Model):
    integrante = models.ForeignKey("Integrante", on_delete=models.CASCADE)
    fecha = models.DateField(default=timezone.now)
    hora  = models.TimeField(default=timezone.now)   # callable OK
    que_hizo_ayer = models.TextField()
    que_hara_hoy  = models.TextField()
    impedimentos  = models.TextField(blank=True, null=True)

    fuera_horario = models.BooleanField(default=False)  # marca ventana 5–9AM

    def __str__(self):
        return f"Daily {self.integrante} - {self.fecha}"
