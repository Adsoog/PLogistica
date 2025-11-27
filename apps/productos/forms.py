from django import forms
from .models import Categoria, Producto


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'