from django.db import models


class Stand(models.Model):
    ESTADOS = [
        ('Disponible', 'Disponible'),
        ('Asignado', 'Asignado'),
    ]

    numero_stand = models.CharField(max_length=20, unique=True)
    ubicacion_mapa = models.CharField(max_length=255)
    estado = models.CharField(max_length=15, choices=ESTADOS, default='Disponible')

    artesano = models.OneToOneField(
        'artesanos.Artesano',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='stand_asignado'
    )

    def __str__(self):
        return f"Stand {self.numero_stand} - {self.estado}"
