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
