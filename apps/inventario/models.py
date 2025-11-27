from django.db import models
from apps.almacen.models import Almacen
from apps.compraventa.models import Compra, Venta
from apps.productos.models import Producto


class Existencias(models.Model):
    producto = models.ForeignKey(
        Producto, 
        verbose_name="Producto", 
        on_delete=models.CASCADE, 
        related_name="existencias"
    )
    almacen = models.ForeignKey(
        Almacen, 
        verbose_name="Almacen", 
        on_delete=models.CASCADE, 
        related_name="existencias"
    )
    cantidad = models.DecimalField("Cantidad del Producto", max_digits=15, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Existencia"
        verbose_name_plural = "Existencias"
        unique_together = ('producto', 'almacen')

    def __str__(self):
        return f"{self.producto.nombre} en {self.almacen.nombre}: {self.cantidad}"


class Movimiento(models.Model):
    class TipoMovimiento(models.TextChoices):
        IN = 'ENTRADA', 'Entrada'
        OUT = 'SALIDA', 'Salida'
        AJUSTE = 'AJUSTE', 'Ajuste'
    
    compra = models.ForeignKey(
        Compra, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name="movimientos"
    )
    venta = models.ForeignKey(
        Venta, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name="movimientos"
    )
    producto = models.ForeignKey(Producto, verbose_name="Producto", on_delete=models.PROTECT, related_name="movimientos")
    almacen = models.ForeignKey(Almacen, verbose_name="Almacén", on_delete=models.PROTECT, related_name="movimientos")
    fecha = models.DateTimeField("Fecha del movimiento", auto_now_add=True, db_index=True)
    tipo = models.CharField("Tipo de Movimiento", max_length=10, choices=TipoMovimiento.choices)
    cantidad = models.DecimalField(max_digits=10, default=0, decimal_places=2)
    motivo = models.CharField("Motivo", max_length=255, blank=True)

    class Meta:
        verbose_name = "Movimiento de inventario"
        verbose_name_plural = "Movimientos de inventario"
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.cantidad} x {self.producto.nombre}"
    