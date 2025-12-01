from django import forms
from django.forms import inlineformset_factory
from apps.compraventa.models import Compra, CompraItem


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
    Compra,
    CompraItem,
    fields=('producto', 'cantidad', 'precio_costo'),
    extra=1,
    can_delete=True
)
