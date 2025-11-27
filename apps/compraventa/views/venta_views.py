from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from apps.productos.models import Producto
from ..models import  Venta, VentaItem
from ..forms import (
    VentaForm, VentaItemForm, VentaItemFormSet
)


class VentaListView(ListView):
    model = Venta
    template_name = 'compraventa/pages/venta_list.html'
    context_object_name = 'ventas'


def venta_detail(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    context = {
        'venta': venta
    }
    return render(request, 'compraventa/pages/venta_detail.html', context)


def venta_create(request):
    form = VentaForm(request.POST or None)
    formset = VentaItemFormSet(request.POST or None)
    
    if request.method == 'POST':
        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    venta = form.save()
                    formset.instance = venta
                    formset.save()
                messages.success(request, 'Venta creada exitosamente.')
                return redirect('venta-list')
            except Exception as e:
                messages.error(request, f'Error al guardar la venta: {e}')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')

    context = {
        'form': form,
        'formset': formset,
        'object': None
    }
    return render(request, 'compraventa/pages/venta_form.html', context)


def venta_edit(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    form = VentaForm(request.POST or None, instance=venta)
    formset = VentaItemFormSet(request.POST or None, instance=venta)
    
    if request.method == 'POST':
        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    venta = form.save()
                    formset.instance = venta
                    formset.save()
                messages.success(request, 'Venta actualizada exitosamente.')
                return redirect('venta-list')
            except Exception as e:
                messages.error(request, f'Error al actualizar la venta: {e}')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')

    context = {
        'form': form,
        'formset': formset,
        'object': venta
    }
    return render(request, 'compraventa/pages/venta_form.html', context)


def venta_delete(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    if request.method == 'POST':
        try:
            venta.delete()
            messages.success(request, 'Venta eliminada exitosamente.')
            return redirect('venta-list')
        except Exception as e:
            messages.error(request, f'Error al eliminar: {e}')
            return redirect('venta-detail', pk=pk)
            
    context = {'object': venta}
    return render(request, 'compraventa/pages/venta_confirm_delete.html', context)


# Vistas dinamicas para la venta porsiblemetne serna las oficiales 
def venta_dinamica_create(request):
    venta = Venta.objects.create(
        fecha=timezone.now().date()
    )
    return redirect('venta-dinamica-detail', pk=venta.pk)
    

def venta_dinamica_detail(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    items = venta.items.all()
    for item in items:
        item.form = VentaItemForm(instance=item)
    context = {
        'venta': venta,
        'items': items,
    }
    return render(request, 'compraventa/pages/venta_dinamica_detail.html', context)


def venta_dinamica_item_create(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    codigo = request.POST.get('codigo_barra')
    producto = Producto.objects.filter(
        Q(codigo_barra=codigo) | Q(sku=codigo)
    ).first()
    context = {'venta': venta, 'error': None}
    if producto:
        item, created = VentaItem.objects.get_or_create(
            venta=venta, 
            producto=producto,
            defaults={'precio_venta': producto.costo_venta, 'cantidad': 0}
        )
        item.cantidad += 1
        item.precio_venta = producto.costo_venta
        item.save() 
    else:
        context['error'] = f"Producto con código o SKU '{codigo}' no encontrado."
    venta.refresh_from_db()
    items = venta.items.all()
    for item in items:
        item.form = VentaItemForm(instance=item)
    context['items'] = items
    return render(request, 'compraventa/partials/venta_items_table.html', context)


def venta_item_update(request, pk):
    item = get_object_or_404(VentaItem, pk=pk)
    if 'cantidad' in request.POST:
        item.cantidad = request.POST.get('cantidad')
    if 'precio_venta' in request.POST:
        item.precio_venta = request.POST.get('precio_venta')
    item.save()
    venta = item.venta
    venta.refresh_from_db()
    
    return render(request, 'compraventa/partials/venta_items_table.html', {'venta': venta})

def venta_item_delete(request, pk):
    item = get_object_or_404(VentaItem, pk=pk)
    venta = item.venta
    item.delete()
    venta.refresh_from_db()
    return render(request, 'compraventa/partials/venta_items_table.html', {'venta': venta})