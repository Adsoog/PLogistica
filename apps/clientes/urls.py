from django.urls import path
from . import views

urlpatterns = [
    path('cliente/lista', views.ClienteListView.as_view(), name='cliente-list'),
    path('cliente/crear/', views.cliente_create, name='cliente-create'),
    path('cliente/editar/<int:pk>/', views.cliente_edit, name='cliente-edit'),
    path('cliente/eliminar/<int:pk>/', views.cliente_delete, name='cliente-delete'),
]