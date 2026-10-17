from django.db import models


class Stand(models.Model):
    class EstadoStand(models.TextChoices):
        DISPONIBLE = "Disponible", "Disponible"
        ASIGNADO = "Asignado", "Asignado"
        MANTENIMIENTO = "Mantenimiento", "En Mantenimiento"

    # Identificador único del stand dentro del predio.
    numero_stand = models.CharField(
        max_length=20, 
        unique=True, 
        verbose_name="Número de Stand"
    )

    # Identificador o coordenadas para el mapa/plano interactivo SVG/Canvas en el index.
    ubicacion_mapa = models.CharField(
        max_length=255, 
        verbose_name="Ubicación en el Mapa / Coordenadas SVG"
    )

    # Estado actual del stand.
    estado = models.CharField(
        max_length=20,
        choices=EstadoStand.choices,
        default=EstadoStand.DISPONIBLE,
        verbose_name="Estado del Stand"
    )

    # Relación 1 a 1: Un artesano habilitado puede tener asignado como máximo un stand.
    artesano = models.OneToOneField(
        'artesanos.Artesano',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='stand_asignado',
        verbose_name="Artesano Asignado"
    )

    class Meta:
        verbose_name = "Stand"
        verbose_name_plural = "Stands"
        ordering = ["numero_stand"]

    def __str__(self):
        artesano_str = f" - {self.artesano.nombre_comercial}" if self.artesano else ""
        return f"Stand {self.numero_stand} ({self.get_estado_display()}){artesano_str}"

    # Se sobrescribe el método save() para que al desvincularse o borrarse un artesano (o si se asigna uno nuevo), el campo estado se actualiza de manera automática entre 'Disponible' y 'Asignado', evitando incoherencias en la base de datos.
    def save(self, *args, **kwargs):

        if self.artesano is not None and self.estado == self.EstadoStand.DISPONIBLE:
            # Si se le asigna un artesano y estaba disponible, pasa a Asignado automáticamente
            self.estado = self.EstadoStand.ASIGNADO
        elif self.artesano is None and self.estado == self.EstadoStand.ASIGNADO:
            # Si se quita el artesano, vuelve a estar Disponible automáticamente
            self.estado = self.EstadoStand.DISPONIBLE

        super().save(*args, **kwargs)