from django.db import models

# Create your models here.
class Producto(models.Model):
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return self.name