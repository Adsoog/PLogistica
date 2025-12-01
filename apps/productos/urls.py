from django.urls import path
from . import views

urlpatterns = [
    # Categoria
    path('categoria/lista', views.CategoriaListView.as_view(), name='categoria-list'),
    path('categoria/crear/', views.categoria_create, name='categoria-create'),
    path('categoria/editar/<int:pk>/', views.categoria_edit, name='categoria-edit'),
    path('categoria/eliminar/<int:pk>/', views.categoria_delete, name='categoria-delete'),

    # Producto
    path('producto/lista', views.ProductoListView.as_view(), name='producto-list'),
    path('producto/crear/', views.producto_create, name='producto-create'),
    path('producto/editar/<int:pk>/', views.producto_edit, name='producto-edit'),
    path('producto/eliminar/<int:pk>/', views.producto_delete, name='producto-delete'),


    # Catalog
    path('catalogo/', views.CatalogoListView.as_view(), name='catalogo-list'),
    path('catalogo/detail/<int:pk>/', views.catalogo_detail, name='catalogo-detail'),
    path('catalogo/create/', views.catalogo_create, name='catalogo-create'),
    path('catalogo/edit/<int:pk>/', views.catalogo_edit, name='catalogo-edit'),
    path('catalogo/delete/<int:pk>/', views.catalogo_delete, name='catalogo-delete'),
]