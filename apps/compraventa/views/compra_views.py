from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.contrib import messages
from apps.compraventa.forms.compra_forms import CompraForm, CompraItemFormSet
from apps.compraventa.models import Compra


class CompraListView(ListView):
    model = Compra
    template_name = 'compraventa/pages/compra_list.html'
    context_object_name = 'compras'


def compra_create(request):
    form = CompraForm(request.POST or None)
    formset = CompraItemFormSet(request.POST or None)
    
    if request.method == 'POST':
        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    compra = form.save()
                    formset.instance = compra
                    formset.save()
                messages.success(request, 'Compra creada exitosamente.')
                return redirect('compra-list')
            except Exception as e:
                messages.error(request, f'Error al guardar la compra: {e}')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')

    context = {
        'form': form,
        'formset': formset,
        'object': None
    }
    return render(request, 'compraventa/pages/compra_form.html', context)


def compra_detail(request, pk):
    compra = get_object_or_404(Compra, pk=pk)
    context = {
        'compra': compra
    }
    return render(request, 'compraventa/pages/compra_detail.html', context)


def compra_edit(request, pk):
    compra = get_object_or_404(Compra, pk=pk)
    form = CompraForm(request.POST or None, instance=compra)
    formset = CompraItemFormSet(request.POST or None, instance=compra)
    
    if request.method == 'POST':
        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    compra = form.save()
                    formset.instance = compra
                    formset.save()
                messages.success(request, 'Compra actualizada exitosamente.')
                return redirect('compra-list')
            except Exception as e:
                messages.error(request, f'Error al actualizar la compra: {e}')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')

    context = {
        'form': form,
        'formset': formset,
        'object': compra
    }
    return render(request, 'compraventa/pages/compra_form.html', context)


def compra_delete(request, pk):
    compra = get_object_or_404(Compra, pk=pk)
    if request.method == 'POST':
        try:
            compra.delete()
            messages.success(request, 'Compra eliminada exitosamente.')
            return redirect('compra-list')
        except Exception as e:
            messages.error(request, f'Error al eliminar: {e}')
            return redirect('compra-detail', pk=pk)
    context = {'object': compra}
    return render(request, 'compraventa/pages/compra_confirm_delete.html', context)