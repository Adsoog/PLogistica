from django.db import models
from almacen.models import Almacen

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



class Proveedor(models.Model):
    nombre = models.CharField("Nombre del Proveedor", max_length=255)
    ruc = models.CharField("RUC", max_length=11, null=True, blank=True)
    telefono = models.CharField("Teléfono", max_length=20, null=True, blank=True)

    def __str__(self):
        return self.nombre


class Cliente(models.Model):
    nombre = models.CharField("Nombre del Cliente", max_length=255)
    ruc_dni = models.CharField("RUC/DNI", max_length=11, null=True, blank=True)
    telefono = models.CharField("Teléfono", max_length=20, null=True, blank=True)
    
    def __str__(self):
        return self.nombre
    

class Compra(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, verbose_name="Proveedor")
    fecha = models.DateField("Fecha de la compra")
    numero_documento = models.CharField("N° Factura/Guía", max_length=50, null=True, blank=True)
    total_compra = models.DecimalField(max_digits=12, decimal_places=2, default=0)

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
    
    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"

    def __str__(self):
        return f"Venta {self.id} - {self.cliente.nombre}"

        
class Movimiento(models.Model):
    class TipoMovimiento(models.TextChoices):
        IN = 'ENTRADA', 'Entrada'
        OUT = 'SALIDA', 'Salida'
        AJUSTE = 'AJUSTE', 'Ajuste'
    
    # --- CAMPOS NUEVOS ---
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
    # ---------------------

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
    