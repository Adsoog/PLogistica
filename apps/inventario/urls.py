from django.urls import path
from . import views

urlpatterns = [
    # Existencias (Solo Lista)
    path('existencias/lista', views.ExistenciasListView.as_view(), name='existencias-list'),
    # Movimientos (Lista y Crear)
    path('movimiento/lista', views.MovimientoListView.as_view(), name='movimiento-list'),
    path('movimiento/crear/', views.movimiento_create, name='movimiento-create'),
]