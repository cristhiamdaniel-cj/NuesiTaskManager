# disponibilidad/models.py
from datetime import timedelta, date
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError


# ==============================
# Helpers de fecha
# ==============================
def lunes_de(fecha: date) -> date:
    """Devuelve el lunes de la semana de 'fecha'."""
    return fecha - timedelta(days=fecha.weekday())


# ==============================
# Disponibilidad Semanal
# ==============================
class DisponibilidadSemanal(models.Model):
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="semanas_disponibilidad",
    )
    semana_inicio = models.DateField(help_text="Lunes de la semana")

    # Trazabilidad
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    actualizado_por = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="semanas_disponibilidad_actualizadas",
        help_text="(Opcional) último usuario que editó la semana",
    )

    class Meta:
        unique_together = ("usuario", "semana_inicio")
        ordering = ("-semana_inicio",)
        verbose_name = "Disponibilidad semanal"
        verbose_name_plural = "Disponibilidades semanales"
        # En V2 sí creamos/migramos tablas
        managed = True

    def __str__(self) -> str:
        nombre = self.usuario.get_full_name() or self.usuario.username
        return f"{nombre} - {self.semana_inicio}"

    @staticmethod
    def actual_lunes() -> date:
        """Lunes de la semana actual (según timezone local)."""
        return lunes_de(timezone.localdate())

    @property
    def semana_fin(self) -> date:
        """Domingo (fin) de esta semana."""
        return self.semana_inicio + timedelta(days=6)

    def ensure_dias(self) -> None:
        """
        Garantiza que existan los 7 registros de DisponibilidadDia (L→D).
        Útil tras crear la semana o al abrir el formulario por primera vez.
        """
        existentes = {d.dia_semana for d in self.dias.all()}
        faltantes = [i for i in range(7) if i not in existentes]
        for i in faltantes:
            DisponibilidadDia.objects.create(
                disponibilidad=self,
                dia_semana=i,
                tipo=DisponibilidadDia.Tipo.NO,
            )


# ==============================
# Día de disponibilidad (L→D)
# ==============================
class DisponibilidadDia(models.Model):
    class Dia(models.IntegerChoices):
        LUNES = 0, "Lunes"
        MARTES = 1, "Martes"
        MIERCOLES = 2, "Miércoles"
        JUEVES = 3, "Jueves"
        VIERNES = 4, "Viernes"
        SABADO = 5, "Sábado"
        DOMINGO = 6, "Domingo"

    class Tipo(models.TextChoices):
        SI = "D", "Disponible todo el día"
        NO = "N", "No disponible"
        RANGO = "R", "Rango de disponibilidad"

    disponibilidad = models.ForeignKey(
        DisponibilidadSemanal,
        on_delete=models.CASCADE,
        related_name="dias",
    )
    dia_semana = models.IntegerField(choices=Dia.choices)
    tipo = models.CharField(max_length=1, choices=Tipo.choices, default=Tipo.NO)

    # Solo obligatorios cuando tipo = RANGO
    hora_inicio = models.TimeField(null=True, blank=True)
    hora_fin = models.TimeField(null=True, blank=True)

    notas = models.CharField(max_length=255, blank=True, default="")

    class Meta:
        unique_together = ("disponibilidad", "dia_semana")
        ordering = ("dia_semana",)
        verbose_name = "Día de disponibilidad"
        verbose_name_plural = "Días de disponibilidad"
        managed = True

    def __str__(self) -> str:
        return f"{self.get_dia_semana_display()} · {self.display_largo}"

    # ===== Validaciones =====
    def clean(self):
        """
        - Si es RANGO: requiere horas y hora_fin > hora_inicio.
        - Si no es RANGO: las horas quedan en blanco (None).
        """
        if self.tipo == self.Tipo.RANGO:
            if self.hora_inicio is None or self.hora_fin is None:
                raise ValidationError("Debe indicar hora de inicio y fin para 'Rango'.")
            if self.hora_fin <= self.hora_inicio:
                raise ValidationError("La hora fin debe ser posterior a la hora inicio.")
        else:
            # Limpia horas cuando no aplican
            self.hora_inicio = None
            self.hora_fin = None

    # ===== Displays amigables =====
    @property
    def display_corto(self) -> str:
        if self.tipo == self.Tipo.SI:
            return "Disponible"
        if self.tipo == self.Tipo.NO:
            return "No"
        if self.hora_inicio and self.hora_fin:
            return f"{self.hora_inicio.strftime('%H:%M')}–{self.hora_fin.strftime('%H:%M')}"
        return "Rango"

    @property
    def display_largo(self) -> str:
        if self.tipo == self.Tipo.SI:
            return "Disponible todo el día"
        if self.tipo == self.Tipo.NO:
            return "No disponible"
        if self.hora_inicio and self.hora_fin:
            return f"Disponible de {self.hora_inicio.strftime('%H:%M')} a {self.hora_fin.strftime('%H:%M')}"
        return "Rango (sin horas)"
# --- Compatibilidad temporal con código viejo ---
HorarioDisponibilidad = DisponibilidadDia
