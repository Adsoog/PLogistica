from django import forms

from django.forms import inlineformset_factory

from apps.compraventa.models import Compra, CompraItem, Venta, VentaItem
from apps.inventario.models import Movimiento

# --- Formulario de Compra y sus Items ---

class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['proveedor', 'fecha', 'numero_documento', 'estado']
        widgets = {
            'fecha': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'
            ),
        }

CompraItemFormSet = inlineformset_factory(
    Compra,         # El modelo "Padre"
    CompraItem,     # El modelo "Hijo"
    fields=('producto', 'cantidad', 'precio_costo'), # Campos a mostrar por item
    extra=1,        # Empezar con 1 fila de item vacía
    can_delete=True # Permitir eliminar items existentes
)


# --- Formulario de Venta y sus Items ---

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        # Campos que el usuario llenará en el formulario principal
        fields = ['cliente', 'fecha', 'numero_documento', 'estado']
        widgets = {
            'fecha': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'
            ),
        }

VentaItemFormSet = inlineformset_factory(
    Venta,          # El modelo "Padre"
    VentaItem,      # El modelo "Hijo"
    fields=('producto', 'cantidad', 'precio_venta'), # Campos a mostrar por item
    extra=1,        # Empezar con 1 fila de item vacía
    can_delete=True # Permitir eliminar items existentes
)


class VentaItemForm(forms.ModelForm):
    class Meta:
        model = VentaItem
        fields = ['cantidad', 'precio_venta', 'descuento_porcentaje']
        widgets = {
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control text-center no-arrow', 
                'placeholder': '0'
            }),
            'precio_venta': forms.NumberInput(attrs={
                'class': 'form-control text-end no-arrow', 
                'step': '0.01'
            }),
            'descuento_porcentaje': forms.NumberInput(attrs={
                'class': 'form-control text-end no-arrow', 
                'min': '0', 'max': '100'
            }),
        }


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