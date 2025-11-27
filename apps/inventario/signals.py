from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import F, Sum
from apps.almacen.models import Almacen
from apps.compraventa.models import (
    Compra, Venta, EstadoDocumento, CompraItem, VentaItem
)
from .models import Movimiento, Existencias

@receiver(post_save, sender=CompraItem)
@receiver(post_delete, sender=CompraItem)
def actualizar_total_compra(sender, instance, **kwargs):
    """
    Cada vez que un item de compra se guarda o elimina,
    recalcula el total de la Compra padre.
    """
    compra = instance.compra
    total_calculado = compra.items.aggregate(
        total=Sum(F('cantidad') * F('precio_costo'))
    )['total']
    compra.total_compra = total_calculado or 0
    compra.save(update_fields=['total_compra'])


@receiver(post_save, sender=VentaItem)
@receiver(post_delete, sender=VentaItem)
def actualizar_total_venta(sender, instance, **kwargs):
    """
    Cada vez que un item de venta se guarda o elimina,
    recalcula el total de la Venta padre.
    """
    venta = instance.venta
    total_calculado = venta.items.aggregate(
        total=Sum(F('cantidad') * F('precio_venta'))
    )['total']
    venta.total_venta = total_calculado or 0
    venta.save(update_fields=['total_venta'])


# --- LOGICA DE INVENTARIO (EXISTENTE) ---

@receiver(post_save, sender=Movimiento)
def actualizar_existencias(sender, instance, created, **kwargs):
    
    if not created:
        return

    producto = instance.producto
    almacen = instance.almacen
    cantidad = instance.cantidad

    existencia, created = Existencias.objects.get_or_create(
        producto=producto, 
        almacen=almacen,
        defaults={'cantidad': 0}
    )
    
    if instance.tipo == Movimiento.TipoMovimiento.IN:
        existencia.cantidad = F('cantidad') + cantidad
    elif instance.tipo == Movimiento.TipoMovimiento.OUT:
        existencia.cantidad = F('cantidad') - cantidad
    elif instance.tipo == Movimiento.TipoMovimiento.AJUSTE:
        existencia.cantidad = F('cantidad') + cantidad
    
    existencia.save()


@receiver(post_save, sender=Compra)
def crear_movimientos_compra(sender, instance, **kwargs):
    
    if instance.estado != EstadoDocumento.CONFIRMADA:
        return
    if Movimiento.objects.filter(compra=instance).exists():
        return
        
    almacen = Almacen.objects.first() 
    if not almacen:
        print(f"ADVERTENCIA: No se encontró almacén. Compra {instance.id} no generó movimientos.")
        return

    for item in instance.items.all():
        Movimiento.objects.create(
            compra=instance,
            producto=item.producto,
            almacen=almacen,
            tipo=Movimiento.TipoMovimiento.IN,
            cantidad=item.cantidad,
            motivo=f"Compra Confirmada {instance.id} ({instance.numero_documento})"
        )

@receiver(post_save, sender=Venta)
def crear_movimientos_venta(sender, instance, **kwargs):

    if instance.estado != EstadoDocumento.CONFIRMADA:
        return
    if Movimiento.objects.filter(venta=instance).exists():
        return

    almacen = Almacen.objects.first()
    if not almacen:
        print(f"ADVERTENCIA: No se encontró almacén. Venta {instance.id} no generó movimientos.")
        return

    for item in instance.items.all():
        Movimiento.objects.create(
            venta=instance,
            producto=item.producto,
            almacen=almacen,
            tipo=Movimiento.TipoMovimiento.OUT,
            cantidad=item.cantidad,
            motivo=f"Venta Confirmada {instance.id} ({instance.numero_documento})"
        )