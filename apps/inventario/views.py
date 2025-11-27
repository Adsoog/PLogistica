from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from .models import Existencias, Movimiento
from .forms import MovimientoForm


class ExistenciasListView(ListView):
    model = Existencias
    template_name = 'inventario/pages/existencias_list.html'
    context_object_name = 'existencias'

    def get_queryset(self):
        return Existencias.objects.select_related('producto', 'almacen')


class MovimientoListView(ListView):
    model = Movimiento
    template_name = 'inventario/pages/movimiento_list.html'
    context_object_name = 'movimientos'

    def get_queryset(self):
        return Movimiento.objects.select_related('producto', 'almacen')


def movimiento_create(request):
    if request.method == 'POST':
        form = MovimientoForm(request.POST)
        if form.is_valid():
            movimiento = form.save()
            return render(request, 'inventario/partials/_movimiento_list_rows.html', {'movimiento': movimiento})
    else:
        form = MovimientoForm()
    
    context = {
        'form': form
    }
    return render(request, 'inventario/forms/_movimiento_form.html', context)