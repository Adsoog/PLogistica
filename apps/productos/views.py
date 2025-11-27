from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from apps.productos.forms import CategoriaForm, ProductoForm
from apps.productos.models import Categoria, Producto


class CategoriaListView(ListView):
    model = Categoria
    template_name = 'producto/pages/categoria_list.html'
    context_object_name = 'categorias'


def categoria_create(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            categoria = form.save()
            return render(request, 'producto/partials/_categoria_list_rows.html', {'categoria': categoria})
    else:
        form = CategoriaForm()
    context = {
        'form': form
    }
    return render(request, 'producto/forms/_categoria_form.html', context)


def categoria_edit(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            categoria = form.save()
            return render(request, 'producto/partials/_categoria_list_rows.html', {'categoria': categoria})
    else:
        form = CategoriaForm(instance=categoria)
    context = {
        'form': form,
        'categoria': categoria
    }
    return render(request, 'producto/forms/_categoria_edit.html', context)


def categoria_delete(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'DELETE':
        categoria.delete()
        return HttpResponse(status=200)
    return HttpResponse(status=405)


class ProductoListView(ListView):
    model = Producto
    template_name = 'producto/pages/producto_list.html'
    context_object_name = 'productos'


def producto_create(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save()
            return render(request, 'producto/partials/_producto_list_rows.html', {'producto': producto})
    else:
        form = ProductoForm()
    context = {
        'form': form
    }
    return render(request, 'producto/forms/_producto_form.html', context)


def producto_edit(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            producto = form.save()
            return render(request, 'producto/partials/_producto_list_rows.html', {'producto': producto})
    else:
        form = ProductoForm(instance=producto)
    context = {
        'form': form,
        'producto': producto
    }
    return render(request, 'producto/forms/_producto_edit.html', context)


def producto_delete(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'DELETE':
        producto.delete()
        return HttpResponse(status=200)
    return HttpResponse(status=405)