from django.db import models

# Create your models here.
class Almacen(models.Model):
    nombre = models.CharField("Nombre del almacén", max_length=100)
    ubicacion = models.CharField("Ubicación (opcional)", max_length=255, null=True, blank=True)

    def __str__(self):
        return self.nombre