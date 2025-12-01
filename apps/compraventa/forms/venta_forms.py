from django import forms

from apps.clientes.models import Cliente
from apps.compraventa.models import Venta, VentaItem
from django.forms import inlineformset_factory



class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
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



class VentaGeneralForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['cliente', 'tipo_comprobante', 'fecha']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select fw-bold'}),
            'tipo_comprobante': forms.Select(attrs={'class': 'form-select'}),
            'fecha': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'type': 'date', 'class': 'form-control'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cliente'].queryset = Cliente.objects.all().order_by('nombre')
        self.fields['cliente'].empty_label = "--- Seleccione Cliente ---"