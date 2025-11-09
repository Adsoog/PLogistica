from django import forms
from .models import Movimiento, Compra, Venta

class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['proveedor', 'fecha', 'numero_documento', 'total_compra']
        widgets = {
            'fecha': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'
            ),
        }

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['cliente', 'fecha', 'numero_documento', 'total_venta']
        widgets = {
            'fecha': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'
            ),
        }


class MovimientoForm(forms.ModelForm):
    class Meta:
        model = Movimiento
        fields = ['producto', 'almacen', 'tipo', 'cantidad', 'motivo']

MovimientoCompraFormSet = forms.inlineformset_factory(
    Compra,
    Movimiento,
    fields=('producto', 'almacen', 'cantidad'),
    extra=1,
    can_delete=True,
    widgets={
        'cantidad': forms.NumberInput(attrs={'placeholder': 'Cantidad'}),
    }
)

MovimientoVentaFormSet = forms.inlineformset_factory(
    Venta,
    Movimiento,
    fields=('producto', 'almacen', 'cantidad'),
    extra=1,
    can_delete=True,
    widgets={
        'cantidad': forms.NumberInput(attrs={'placeholder': 'Cantidad'}),
    }
)