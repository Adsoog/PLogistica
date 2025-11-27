from django.urls import path
from . import views

urlpatterns = [
    # Proveedor
    path('proveedor/lista', views.ProveedorListView.as_view(), name='proveedor-list'),
    path('proveedor/crear/', views.proveedor_create, name='proveedor-create'),
    path('proveedor/editar/<int:pk>/', views.proveedor_edit, name='proveedor-edit'),
    path('proveedor/eliminar/<int:pk>/', views.proveedor_delete, name='proveedor-delete'),
]