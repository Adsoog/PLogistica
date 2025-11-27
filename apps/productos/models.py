from django.db import models

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField("Nombre de la categoria", max_length=250)
    descripcion = models.TextField("Descripcion")

    def __str__(self):
        return self.nombre

                                               
class Producto(models.Model):
    sku = models.CharField("SKU", max_length=50, unique=True)
    nombre = models.CharField("Nombre del Producto", max_length=250)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Categoria del producto", related_name="productos")
    descripcion = models.TextField("Descripcion")
    costo_compra = models.DecimalField("Costo de compra", max_digits=12, decimal_places=2, default=0)
    costo_venta = models.DecimalField("Costo de venta", max_digits=12, decimal_places=2, default=0)
    codigo_barra = models.CharField("Codigo de Barra", max_length=25)
    
    def __str__(self):
        return self.nombre