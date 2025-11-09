from django.urls import path
from . import views

app_name = 'almacen'

urlpatterns = [
    path('lista', views.AlmacenListView.as_view(), name='almacen-list'),
    path('crear/', views.almacen_create, name='almacen-create'),
    path('editar/<int:pk>/', views.almacen_edit, name='almacen-edit'),
    path('eliminar/<int:pk>/', views.almacen_delete, name='almacen-delete'),
]