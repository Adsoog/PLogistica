from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Almacen
from .forms import AlmacenForm
from django.views.generic import ListView


class AlmacenListView(ListView):
    model = Almacen
    template_name = 'pages/almacen_list.html'
    context_object_name = 'almacenes'


def almacen_create(request):
    if request.method == 'POST':
        form = AlmacenForm(request.POST)
        if form.is_valid():
            almacen = form.save()
            return render(request, 'partials/_almacen_list_rows.html', {'almacen': almacen})
    else:
        form = AlmacenForm()
    context = {
        'form': form
    }
    return render(request, 'forms/_almacen_form.html', context)


def almacen_edit(request, pk):
    almacen = get_object_or_404(Almacen, pk=pk)
    if request.method == 'POST':
        form = AlmacenForm(request.POST, instance=almacen)
        if form.is_valid():
            almacen = form.save()
            return render(request, 'partials/_almacen_list_rows.html', {'almacen': almacen})
    else:
        form = AlmacenForm(instance=almacen)
    context = {
        'form': form,
        'almacen': almacen
    }
    return render(request, 'forms/_almacen_edit.html', context)


def almacen_delete(request, pk):
    almacen = get_object_or_404(Almacen, pk=pk)
    if request.method == 'DELETE':
        almacen.delete()
        return HttpResponse(status=200)
    return HttpResponse(status=405)