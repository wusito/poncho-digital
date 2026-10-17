from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models


# Opciones según el formulario.
RUBROS_CHOICES = [
    # Arte Textil
    ('textil_telar', 'Tejido en Telar (Criollo / Pedal)'),
    ('textil_hilanderia', 'Hilandería Tradicional'),
    ('textil_randa', 'Randa y Bordado Tradicional'),
    # Rubros Tradicionales
    ('ceramica', 'Cerámica / Alfarería'),
    ('cuero', 'Cuero y Talabartería'),
    ('madera', 'Madera y Luthería (Instrumentos)'),
    ('metal', 'Platería, Cincelado y Metales'),
    ('piedra', 'Piedra y Rodocrosita'),
    ('cesteria', 'Fibras Vegetales / Cestería'),
    # Otros
    ('vidrio', 'Vidrio Artesanal / Vitral'),
    ('jugueteria', 'Juguetería Artesanal'),
    ('papel', 'Papel Artesanal / Cartapesta'),
    ('otro', 'Otro rubro no listado'),
]

DEPARTAMENTOS_CHOICES = [
    ('Ambato', 'Ambato'),
    ('Ancasti', 'Ancasti'),
    ('Andalgala', 'Andalgalá'),
    ('Antofagasta de la Sierra', 'Antofagasta de la Sierra'),
    ('Belen', 'Belén'),
    ('Capayan', 'Capayán'),
    ('Capital', 'Capital'),
    ('El Alto', 'El Alto'),
    ('Fray Mamerto Esquiu', 'Fray Mamerto Esquiú'),
    ('La Paz', 'La Paz'),
    ('Paclin', 'Paclín'),
    ('Poman', 'Pomán'),
    ('Santa Maria', 'Santa María'),
    ('Santa Rosa', 'Santa Rosa'),
    ('Tinogasta', 'Tinogasta'),
    ('Valle Viejo', 'Valle Viejo'),
]

SEXO_CHOICES = [
    ('masculino', 'Masculino'),
    ('femenino', 'Femenino'),
    ('no-binario', 'No binario'),
]


# Modelo: Artesano - HU-01: Solicitud de participación de artesanos.
class Artesano(models.Model):
    """Perfil oficial del artesano habilitado en la plataforma."""

    # Relación 1 a 1 con el usuario nativo de Django.
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="artesano",
        help_text="Cuenta de usuario nativa vinculada al artesano",
    )
    nombre_comercial = models.CharField(max_length=100, unique=True)
    rubro = models.CharField(max_length=50, choices=RUBROS_CHOICES)
    descripcion_emprendimiento = models.TextField(
        help_text="Descripción del proceso productivo y materias primas",
    )
    telefono = models.CharField(max_length=20)
    
    # Procedencia y Domicilio
    provincia = models.CharField(max_length=50, default="Catamarca")
    departamento = models.CharField(max_length=50, choices=DEPARTAMENTOS_CHOICES, blank=True, null=True)
    localidad = models.CharField(max_length=100)
    direccion = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        verbose_name = "Artesano"
        verbose_name_plural = "Artesanos"
        ordering = ["nombre_comercial"]

    def __str__(self):
        return f"{self.nombre_comercial} ({self.get_rubro_display()}) - {self.localidad}"



# Modelo: PostulanteArtesano - HU-01: Solicitud de participación de artesanos.
class PostulanteArtesano(models.Model):
    """Solicitudes enviadas desde el formulario HTML por aspirantes."""

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
        help_text="Se vincula automáticamente cuando la solicitud es aprobada",
    )

    # Sección 1: Emprendimiento.
    nombre_emprendimiento = models.CharField(max_length=100)
    rubro_principal = models.CharField(max_length=50, choices=RUBROS_CHOICES)
    descripcion_proceso = models.TextField(help_text="Descripción del proceso y materias primas")

    # Sección 2: Datos Personales.
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=8, unique=True)
    cuit_o_cuil = models.CharField(max_length=11, verbose_name="CUIT/CUIL")
    fecha_nacimiento = models.DateField()
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    sexo = models.CharField(max_length=20, choices=SEXO_CHOICES)

    # Sección 3: Procedencia y Domicilio.
    provincia = models.CharField(max_length=50, default="Catamarca")
    departamento = models.CharField(max_length=50, choices=DEPARTAMENTOS_CHOICES, blank=True, null=True)
    localidad = models.CharField(max_length=100)
    direccion = models.CharField(max_length=150, blank=True, null=True)

    # Sección 4: Términos y Estado.
    terminos_condiciones = models.BooleanField(default=True)
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

    def __str__(self):
        return f"{self.apellido}, {self.nombre} - {self.nombre_emprendimiento} [{self.get_estado_solicitud_display()}]"



# Modelo: Calidicacion - HU-10: Registro de calificaciones y comentarios.
class Calificacion(models.Model):
    """Calificaciones y comentarios de los visitantes hacia los artesanos."""

    artesano = models.ForeignKey(
        Artesano,
        on_delete=models.CASCADE,
        related_name="calificaciones",
        verbose_name="Artesano",
    )
    nombre_visitante = models.CharField(
        max_length=100, verbose_name="Nombre del visitante"
    )
    email_visitante = models.EmailField(verbose_name="Correo electrónico")
    puntuacion = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Calificación de 1 a 5 estrellas",
        verbose_name="Puntuación",
    )
    comentario = models.TextField(verbose_name="Comentario")
    fecha_creacion = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de publicación"
    )

    class Meta:
        verbose_name = "Calificación"
        verbose_name_plural = "Calificaciones"
        ordering = ["-fecha_creacion"]

    def __str__(self):
        return f"Calificación de {self.puntuacion}★ por {self.nombre_visitante} a {self.artesano.nombre_comercial}"


# Modelo: Consulta - HU-11: Registro y Respuesta de consultas.
class Consulta(models.Model):
    """Consultas enviadas por los visitantes a un artesano y su respuesta."""

    class EstadoConsulta(models.TextChoices):
        PENDIENTE = "PENDIENTE", "Pendiente"
        RESPONDIDA = "RESPONDIDA", "Respondida"

    artesano = models.ForeignKey(
        Artesano,
        on_delete=models.CASCADE,
        related_name="consultas",
        verbose_name="Artesano",
    )
    nombre_visitante = models.CharField(
        max_length=100, verbose_name="Nombre del visitante"
    )
    email_visitante = models.EmailField(verbose_name="Correo electrónico")
    mensaje = models.TextField(verbose_name="Consulta / Mensaje")
    respuesta_artesano = models.TextField(
        blank=True, null=True, verbose_name="Respuesta del artesano"
    )
    estado = models.CharField(
        max_length=10,
        choices=EstadoConsulta.choices,
        default=EstadoConsulta.PENDIENTE,
        verbose_name="Estado",
    )
    fecha_consulta = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de consulta"
    )
    fecha_respuesta = models.DateTimeField(
        blank=True, null=True, verbose_name="Fecha de respuesta"
    )

    class Meta:
        verbose_name = "Consulta"
        verbose_name_plural = "Consultas"
        ordering = ["-fecha_consulta"]

    def __str__(self):
        return f"Consulta de {self.nombre_visitante} a {self.artesano.nombre_comercial} [{self.get_estado_display()}]"