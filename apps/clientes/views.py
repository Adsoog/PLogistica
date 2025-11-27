from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from .models import Cliente
from .forms import ClienteForm


# Create your views here.
class ClienteListView(ListView):
    model = Cliente
    template_name = 'cliente/pages/cliente_list.html'
    context_object_name = 'clientes'


def cliente_create(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            return render(request, 'cliente/partials/_cliente_list_rows.html', {'cliente': cliente})
    else:
        form = ClienteForm()
    context = {
        'form': form
    }
    return render(request, 'cliente/forms/_cliente_form.html', context)


def cliente_edit(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            cliente = form.save()
            return render(request, 'cliente/partials/_cliente_list_rows.html', {'cliente': cliente})
    else:
        form = ClienteForm(instance=cliente)
    context = {
        'form': form,
        'cliente': cliente
    }
    return render(request, 'cliente/forms/_cliente_edit.html', context)


def cliente_delete(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'DELETE':
        cliente.delete()
        return HttpResponse(status=200)
    return HttpResponse(status=405)