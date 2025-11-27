from django.db import models

# Create your models here.
class Proveedor(models.Model):
    nombre = models.CharField("Nombre del Proveedor", max_length=255)
    ruc = models.CharField("RUC", max_length=11, null=True, blank=True)
    telefono = models.CharField("Teléfono", max_length=20, null=True, blank=True)

    def __str__(self):
        return self.nombre