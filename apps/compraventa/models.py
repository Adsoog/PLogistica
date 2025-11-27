from django.db import models
from apps.clientes.models import Cliente
from apps.productos.models import Producto
from apps.proveedores.models import Proveedor


class EstadoDocumento(models.TextChoices):
    BORRADOR = 'BORRADOR', 'Borrador'
    CONFIRMADA = 'CONFIRMADA', 'Confirmada'
    RECHAZADA = 'RECHAZADA', 'Rechazada'


class Compra(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, verbose_name="Proveedor")
    fecha = models.DateField("Fecha de la compra")
    numero_documento = models.CharField("N° Factura/Guía", max_length=50, null=True, blank=True)
    total_compra = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    estado = models.CharField("Estado", max_length=20, choices=EstadoDocumento.choices, default=EstadoDocumento.BORRADOR)

    class Meta:
        verbose_name = "Compra"
        verbose_name_plural = "Compras"

    def __str__(self):
        return f"Compra {self.id} - {self.proveedor.nombre}"


class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, verbose_name="Cliente")
    fecha = models.DateField("Fecha de la venta")
    numero_documento = models.CharField("N° Boleta/Factura", max_length=50, null=True, blank=True)
    total_venta = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    estado = models.CharField("Estado", max_length=20, choices=EstadoDocumento.choices, default=EstadoDocumento.BORRADOR)

    def calcular_total(self):
        """
        Recorre todos los items, suma sus subtotales y guarda el resultado.
        """
        total = sum(item.subtotal for item in self.items.all())
        self.total_venta = total
        self.save()

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"

    def __str__(self):
        return f"Venta {self.id} - {self.cliente.nombre}"


class CompraItem(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name="items")
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    precio_costo = models.DecimalField(max_digits=12, decimal_places=2)
    
    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"


class VentaItem(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name="items")
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    precio_venta = models.DecimalField(max_digits=12, decimal_places=2)
    descuento_porcentaje = models.DecimalField("Descuento %", max_digits=5, decimal_places=2, default=0)

    @property
    def subtotal(self):
        """Calcula el total de la linea aplicando descuento"""
        bruto = self.cantidad * self.precio_venta
        descuento = bruto * (self.descuento_porcentaje / 100)
        return bruto - descuento

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.venta.calcular_total()

    def delete(self, *args, **kwargs):
        venta_ref = self.venta 
        super().delete(*args, **kwargs)
        venta_ref.calcular_total()

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"