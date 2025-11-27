from django.urls import path
from .views import venta_views, compra_views

urlpatterns = []

comprapatterns = [
    path('compra/lista/', compra_views.CompraListView.as_view(), name='compra-list'),
    path('compra/nueva/', compra_views.compra_create, name='compra-create'),
    path('compra/<int:pk>/', compra_views.compra_detail, name='compra-detail'),
    path('compra/<int:pk>/editar/', compra_views.compra_edit, name='compra-edit'),
    path('compra/<int:pk>/eliminar/', compra_views.compra_delete, name='compra-delete'),
]

ventapatterns = [
    path('venta/lista/', venta_views.VentaListView.as_view(), name='venta-list'),
    path('venta/nueva/', venta_views.venta_create, name='venta-create'),
    path('venta/<int:pk>/', venta_views.venta_detail, name='venta-detail'),
    path('venta/<int:pk>/editar/', venta_views.venta_edit, name='venta-edit'),
    path('venta/<int:pk>/eliminar/', venta_views.venta_delete, name='venta-delete'),
    # Dinamic views
    path('venta/dinamica/nueva/', venta_views.venta_dinamica_create, name='venta-dinamica-create'),
    path('venta/dinamica/detalle/<int:pk>/', venta_views.venta_dinamica_detail, name='venta-dinamica-detail'),
    path('venta/dinamica/item/add/<int:pk>/', venta_views.venta_dinamica_item_create, name='venta-dinamica-item-create'),
    path('venta/item/update/<int:pk>/', venta_views.venta_item_update, name='venta-item-update'),
    path('venta/item/delete/<int:pk>/', venta_views.venta_item_delete, name='venta-item-delete'),
]


urlpatterns += comprapatterns
urlpatterns += ventapatterns