from django.db import transaction
from django.http import HttpResponseRedirect
from .models import Compra, Venta
from .forms import CompraForm, MovimientoCompraFormSet, MovimientoVentaFormSet, VentaForm
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from .models import (
    Producto, Categoria, Almacen, Existencias, Movimiento, 
    Proveedor, Cliente
)
from .forms import MovimientoForm


class ProductoListView(ListView):
    model = Producto
    template_name = 'inventario/producto_list.html'
    context_object_name = 'productos'


class ProductoCreateView(CreateView):
    model = Producto
    template_name = 'inventario/producto_form.html'
    fields = ['sku', 'nombre', 'categoria', 'descripcion', 'costo_compra', 'costo_venta', 'codigo_barra']
    success_url = reverse_lazy('inventario:producto-list')


class ProductoUpdateView(UpdateView):
    model = Producto
    template_name = 'inventario/producto_form.html'
    fields = ['sku', 'nombre', 'categoria', 'descripcion', 'costo_compra', 'costo_venta', 'codigo_barra']
    success_url = reverse_lazy('inventario:producto-list')




class CategoriaListView(ListView):
    model = Categoria
    template_name = 'inventario/categoria_list.html'
    context_object_name = 'categorias'


class CategoriaCreateView(CreateView):
    model = Categoria
    template_name = 'inventario/categoria_form.html'
    fields = ['nombre', 'descripcion']
    success_url = reverse_lazy('inventario:categoria-list')


class CategoriaUpdateView(UpdateView):
    model = Categoria
    template_name = 'inventario/categoria_form.html'
    fields = ['nombre', 'descripcion']
    success_url = reverse_lazy('inventario:categoria-list')


class ExistenciasListView(ListView):
    model = Existencias
    template_name = 'inventario/existencias_list.html'
    context_object_name = 'existencias'
    ordering = ['producto__nombre']


class MovimientoCreateView(CreateView):
    model = Movimiento
    form_class = MovimientoForm
    template_name = 'inventario/movimiento_form.html'
    success_url = reverse_lazy('inventario:existencias-list')


class MovimientoListView(ListView):
    model = Movimiento
    template_name = 'inventario/movimiento_list.html'
    context_object_name = 'movimientos'
    ordering = ['-fecha']


class ProveedorListView(ListView):
    model = Proveedor
    template_name = 'inventario/proveedor_list.html'
    context_object_name = 'proveedores'


class ProveedorCreateView(CreateView):
    model = Proveedor
    template_name = 'inventario/proveedor_form.html'
    fields = ['nombre', 'ruc', 'telefono']
    success_url = reverse_lazy('inventario:proveedor-list')


class ProveedorUpdateView(UpdateView):
    model = Proveedor
    template_name = 'inventario/proveedor_form.html'
    fields = ['nombre', 'ruc', 'telefono']
    success_url = reverse_lazy('inventario:proveedor-list')


class ClienteListView(ListView):
    model = Cliente
    template_name = 'inventario/cliente_list.html'
    context_object_name = 'clientes'


class ClienteCreateView(CreateView):
    model = Cliente
    template_name = 'inventario/cliente_form.html'
    fields = ['nombre', 'ruc_dni', 'telefono']
    success_url = reverse_lazy('inventario:cliente-list')


class ClienteUpdateView(UpdateView):
    model = Cliente
    template_name = 'inventario/cliente_form.html'
    fields = ['nombre', 'ruc_dni', 'telefono']
    success_url = reverse_lazy('inventario:cliente-list')


class CompraListView(ListView):
    model = Compra
    template_name = 'inventario/compra_list.html'
    context_object_name = 'compras'
    ordering = ['-fecha']


class CompraCreateView(CreateView):
    model = Compra
    template_name = 'inventario/compra_form.html'
    form_class = CompraForm
    success_url = reverse_lazy('inventario:compra-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = MovimientoCompraFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = MovimientoCompraFormSet(instance=self.object)
            context['formset'].extra = 3 
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        if not form.is_valid() or not formset.is_valid():
            return self.form_invalid(form)

        with transaction.atomic():
            self.object = form.save() 
            
            movimientos = formset.save(commit=False)
            for mov in movimientos:
                mov.tipo = Movimiento.TipoMovimiento.IN
                mov.compra = self.object
                mov.save() 

        return HttpResponseRedirect(self.get_success_url())


class VentaListView(ListView):
    model = Venta
    template_name = 'inventario/venta_list.html'
    context_object_name = 'ventas'
    ordering = ['-fecha']


class VentaCreateView(CreateView):
    model = Venta
    template_name = 'inventario/venta_form.html'
    form_class = VentaForm
    success_url = reverse_lazy('inventario:venta-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = MovimientoVentaFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = MovimientoVentaFormSet(instance=self.object)
            context['formset'].extra = 3
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        if not form.is_valid() or not formset.is_valid():
            return self.form_invalid(form)

        with transaction.atomic():
            self.object = form.save()
            
            movimientos = formset.save(commit=False)
            for mov in movimientos:
                mov.tipo = Movimiento.TipoMovimiento.OUT
                mov.venta = self.object
                mov.save() 

        return HttpResponseRedirect(self.get_success_url())