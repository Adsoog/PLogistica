from django.db import models

# Create your models here.
class Cliente(models.Model):
    nombre = models.CharField("Nombre del Cliente", max_length=255)
    ruc_dni = models.CharField("RUC/DNI", max_length=11, null=True, blank=True)
    telefono = models.CharField("Teléfono", max_length=20, null=True, blank=True)
    email = models.EmailField("Correo electronico", null=True, blank=True)
    
    def __str__(self):
        return self.nombre