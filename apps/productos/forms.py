from django import forms
from .models import Catalogo, Categoria, Producto


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'


class CatalogoForm(forms.ModelForm):
    class Meta:
        model = Catalogo
        fields = ['titulo', 'header_img', 'footer_img', 'fondo_color', 'productos']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'fondo_color': forms.TextInput(attrs={'type': 'color', 'class': 'form-control form-control-color'}),
            'productos': forms.SelectMultiple(attrs={'class': 'form-select', 'style': 'height: 200px;'}),
            'header_img': forms.FileInput(attrs={'class': 'form-control'}),
            'footer_img': forms.FileInput(attrs={'class': 'form-control'}),
        }