from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    # APPS
    path('', include('apps.casa.urls')),
    path('inventario', include('apps.inventario.urls')),
    path('almacen/', include('apps.almacen.urls')),
    path('clientes/', include('apps.clientes.urls')),
    path('documentos/', include('apps.compraventa.urls')),
    path('contabilidad/', include('apps.contabilidad.urls')),
    path('productos/', include('apps.productos.urls')),
    path('proveedores/', include('apps.proveedores.urls')),
]
