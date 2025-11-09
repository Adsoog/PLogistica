from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    path('productos/', views.ProductoListView.as_view(), name='producto-list'),
    path('productos/nuevo/', views.ProductoCreateView.as_view(), name='producto-create'),
    path('productos/<int:pk>/editar/', views.ProductoUpdateView.as_view(), name='producto-update'),
    
    path('categorias/', views.CategoriaListView.as_view(), name='categoria-list'),
    path('categorias/nueva/', views.CategoriaCreateView.as_view(), name='categoria-create'),
    path('categorias/<int:pk>/editar/', views.CategoriaUpdateView.as_view(), name='categoria-update'),

    path('proveedores/', views.ProveedorListView.as_view(), name='proveedor-list'),
    path('proveedores/nuevo/', views.ProveedorCreateView.as_view(), name='proveedor-create'),
    path('proveedores/<int:pk>/editar/', views.ProveedorUpdateView.as_view(), name='proveedor-update'),

    path('clientes/', views.ClienteListView.as_view(), name='cliente-list'),
    path('clientes/nuevo/', views.ClienteCreateView.as_view(), name='cliente-create'),
    path('clientes/<int:pk>/editar/', views.ClienteUpdateView.as_view(), name='cliente-update'),

    path('', views.ExistenciasListView.as_view(), name='existencias-list'),

    path('compras/', views.CompraListView.as_view(), name='compra-list'),
    path('compras/nueva/', views.CompraCreateView.as_view(), name='compra-create'),
    
    path('ventas/', views.VentaListView.as_view(), name='venta-list'),
    path('ventas/nueva/', views.VentaCreateView.as_view(), name='venta-create'),
    
    path('movimientos/nuevo/', views.MovimientoCreateView.as_view(), name='movimiento-create'),
    path('movimientos/historial/', views.MovimientoListView.as_view(), name='movimiento-list'),
]