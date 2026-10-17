from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models


class Artesano(models.Model):
    """Artesanos que ofrecen sus productos en la plataforma."""

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="artesanos",
        help_text="Cuenta de usuario vinculada al artesano",
    )
    nombre_comercial = models.CharField(max_length=100, unique=True)
    descripcion_emprendimiento = models.TextField(
        max_length=500,
        help_text="Ingrese la descripción del emprendimiento",
    )
    telefono = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r"^\+?\d{7,15}$",
                message="Ingrese un teléfono válido (solo números, opcional +).",
            )
        ],
        help_text="Teléfono de contacto",
    )

    class Meta:
        verbose_name = "Artesano"
        verbose_name_plural = "Artesanos"
        ordering = ["nombre_comercial"]

    def __str__(self):
        return f"{self.nombre_comercial} - tel: {self.telefono}"


class PostulanteArtesano(models.Model):
    """Solicitudes de personas que quieren registrarse como artesanos."""

    class EstadoSolicitud(models.TextChoices):
        PENDIENTE = "PENDIENTE", "Pendiente"
        APROBADO = "APROBADO", "Aprobado"
        RECHAZADO = "RECHAZADO", "Rechazado"

    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="postulacion_artesano",
        help_text="Se vincula cuando la solicitud es aprobada",
    )
    # Datos personales
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=15, unique=True)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)

    nombre_emprendimiento = models.CharField(max_length=100)
    estado_solicitud = models.CharField(
        max_length=10,
        choices=EstadoSolicitud.choices,
        default=EstadoSolicitud.PENDIENTE,
    )
    fecha_solicitud = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Postulante a artesano"
        verbose_name_plural = "Postulantes a artesanos"
        ordering = ["-fecha_solicitud"]
        constraints = [
            models.CheckConstraint(
                condition=(
                        models.Q(estado_solicitud="APROBADO")
                        | models.Q(usuario__isnull=True)
                ),
                name="postulante_usuario_solo_si_aprobado",
            ),
        ]

    def __str__(self):
        return (
            f"{self.apellido}, {self.nombre} - "
            f"{self.nombre_emprendimiento} ({self.get_estado_solicitud_display()})"
        )


