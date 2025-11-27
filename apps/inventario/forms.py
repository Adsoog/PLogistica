from django import forms
from apps.inventario.models import Movimiento


class MovimientoForm(forms.ModelForm):
    class Meta:
        model = Movimiento
        fields = ['producto', 'almacen', 'tipo', 'cantidad', 'motivo']