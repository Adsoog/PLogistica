# inventario/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import F
from .models import Movimiento, Existencias

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