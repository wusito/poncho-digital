from django.db import models
from django.core.validators import MinValueValidator
from apps.artesanos.models import Artesano  # Importamos el modelo Artesano.

# Create your models here.
class Producto(models.Model):
    # Opciones para el campo 'categoria' extraídas exactamente de tu HTML.
    CATEGORIAS = [
        ('textiles-tradicionales', 'Textiles Tradicionales'),
        ('artesanias-articulos-hogar', 'Artesanías y Artículos para el Hogar'),
        ('productos-regionales-delicatessen', 'Productos Regionales y Delicatessen'),
        ('sector-comercial', 'Sector Comercial'),
    ]

    # Relación 1:N - Un artesano tiene muchos productos. Eliminación en cascada.
    artesano = models.ForeignKey(
        Artesano, 
        on_delete=models.CASCADE, 
        related_name='productos',
        verbose_name="Artesano"
    )

    # Atributo indexado para búsquedas rápidas (db_index=True)
    nombre = models.CharField(
        max_length=150, 
        db_index=True, 
        verbose_name="Nombre del producto"
    )

    descripcion = models.TextField(
        verbose_name="Descripción del producto"
    )

    categoria = models.CharField(
        max_length=100, 
        choices=CATEGORIAS, 
        verbose_name="Categoría"
    )

    subcategoria = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        verbose_name="Subcategoría"
    )

    # Stock validado para no permitir valores negativos.
    stock = models.PositiveIntegerField(
        default=0,
        verbose_name="Stock disponible"
    )

    # Precio con validación de valor mínimo positivo (> 0).
    precio_unitario = models.DecimalField(
        max_length=10, 
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name="Precio por unidad"
    )

    # Imagen del producto (sube a la carpeta media/productos/).
    imagen = models.ImageField(
        upload_to='productos/', 
        verbose_name="Imagen del producto"
    )

    # Marcas de tiempo de auditoría.
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"{self.nombre} - ${self.precio_unitario}"