from django.db import models
from apps.clientes.models import Cliente
from apps.productos.models import Producto
from apps.proveedores.models import Proveedor


class TipoComprobante(models.TextChoices):
    BOLETA = 'BOLETA', 'Boleta'
    FACTURA = 'FACTURA', 'Factura'


class EstadoDocumento(models.TextChoices):
    BORRADOR = 'BORRADOR', 'Borrador'
    CONFIRMADA = 'CONFIRMADA', 'Confirmada'
    RECHAZADA = 'RECHAZADA', 'Rechazada'


class Compra(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, verbose_name="Proveedor")
    fecha = models.DateField("Fecha de la compra")
    numero_documento = models.CharField("N° Factura/Guía", max_length=50, null=True, blank=True)
    tipo_comprobante = models.CharField(max_length=10, choices=TipoComprobante.choices, default=TipoComprobante.BOLETA)
    total_compra = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    estado = models.CharField("Estado", max_length=20, choices=EstadoDocumento.choices, default=EstadoDocumento.BORRADOR)

    class Meta:
        verbose_name = "Compra"
        verbose_name_plural = "Compras"

    def __str__(self):
        return f"Compra {self.id} - {self.proveedor.nombre}"


class CompraItem(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name="items")
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    precio_costo = models.DecimalField(max_digits=12, decimal_places=2)
    
    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"


class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, verbose_name="Cliente")
    fecha = models.DateField("Fecha de la venta")
    tipo_comprobante = models.CharField(max_length=10, choices=TipoComprobante.choices, default=TipoComprobante.BOLETA)
    numero_documento = models.CharField("N° Documento", max_length=50, null=True, blank=True, unique=True)
    total_venta = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    estado = models.CharField("Estado", max_length=20, choices=EstadoDocumento.choices, default=EstadoDocumento.BORRADOR)

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"

    def __str__(self):
        return f"{self.numero_documento or 'Borrador'} - {self.cliente}"

    def calcular_total(self):
        total = sum(item.subtotal for item in self.items.all())
        self.total_venta = total
        self.save()

    def confirmar_venta(self):
        if not self.numero_documento:
            self.numero_documento = self._generar_correlativo()
        self.estado = EstadoDocumento.CONFIRMADA
        self.save()

    def _generar_correlativo(self):
        prefix = 'B001' if self.tipo_comprobante == TipoComprobante.BOLETA else 'F001'
        ultima_venta = Venta.objects.filter(
            tipo_comprobante=self.tipo_comprobante,
            numero_documento__isnull=False
        ).order_by('numero_documento').last()
        if not ultima_venta:
            return f"{prefix}-00000001"
        ultimo_numero = int(ultima_venta.numero_documento.split('-')[1])
        nuevo_numero = ultimo_numero + 1
        return f"{prefix}-{str(nuevo_numero).zfill(8)}"


class VentaItem(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name="items")
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    precio_venta = models.DecimalField(max_digits=12, decimal_places=2)
    descuento_porcentaje = models.DecimalField("Descuento %", max_digits=5, decimal_places=2, default=0)

    @property
    def diferencia_precio(self):
        """
        Calcula la diferencia entre el precio al que estás vendiendo
        y el precio de lista original del producto.
        Ej: Lista 20, Venta 28 -> Retorna +8
        Ej: Lista 25, Venta 23 -> Retorna -2
        """
        return self.precio_venta - self.producto.costo_venta

    @property
    def ganancia_extra_total(self):
        """Calcula esa diferencia multiplicada por la cantidad"""
        return self.diferencia_precio * self.cantidad

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