from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from .models import Proveedor
from .forms import ProveedorForm

# Create your views here.
class ProveedorListView(ListView):
    model = Proveedor
    template_name = 'proveedor/pages/proveedor_list.html'
    context_object_name = 'proveedores'


def proveedor_create(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            proveedor = form.save()
            return render(request, 'proveedor/partials/_proveedor_list_rows.html', {'proveedor': proveedor})
    else:
        form = ProveedorForm()
    context = {
        'form': form
    }
    return render(request, 'proveedor/forms/_proveedor_form.html', context)


def proveedor_edit(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            proveedor = form.save()
            return render(request, 'proveedor/partials/_proveedor_list_rows.html', {'proveedor': proveedor})
    else:
        form = ProveedorForm(instance=proveedor)
    context = {
        'form': form,
        'proveedor': proveedor
    }
    return render(request, 'proveedor/forms/_proveedor_edit.html', context)


def proveedor_delete(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'DELETE':
        proveedor.delete()
        return HttpResponse(status=200)
    return HttpResponse(status=405)