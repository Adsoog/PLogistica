from django import forms

from django.forms import inlineformset_factory

from apps.compraventa.models import Compra, CompraItem, Venta, VentaItem
from apps.inventario.models import Movimiento


# --- Formulario de Movimiento (Para Ajustes) ---

class MovimientoForm(forms.ModelForm):
    class Meta:
        model = Movimiento
        # Campos para el formulario de "Nuevo Movimiento" (Ajustes)
        fields = ['producto', 'almacen', 'tipo', 'cantidad', 'motivo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Opcional: Limitar el "tipo" solo a Ajuste si este form es solo para eso
        self.fields['tipo'].choices = [
            ('AJUSTE', 'Ajuste'),
            ('ENTRADA', 'Entrada (Manual)'),
            ('SALIDA', 'Salida (Manual)'),
        ]
        self.fields['tipo'].initial = 'AJUSTE'