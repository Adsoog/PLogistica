from django.db import models

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField("Nombre de la categoria", max_length=250)
    descripcion = models.TextField("Descripcion")

    def __str__(self):
        return self.nombre

                                               
class Producto(models.Model):
    sku = models.CharField("SKU", max_length=50, unique=True)
    nombre = models.CharField("Nombre del Producto", max_length=250)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Categoria del producto", related_name="productos")
    descripcion = models.TextField("Descripcion")
    costo_compra = models.DecimalField("Costo de compra", max_digits=12, decimal_places=2, default=0)
    costo_venta = models.DecimalField("Costo de venta", max_digits=12, decimal_places=2, default=0)
    codigo_barra = models.CharField("Codigo de Barra", max_length=25)
    imagen = models.ImageField("Imagen", upload_to='productos/', null=True, blank=True)

    
    def __str__(self):
        return self.nombre
    

class Catalogo(models.Model):
    titulo = models.CharField("Título de Campaña", max_length=150)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    header_img = models.ImageField("Banner Superior", upload_to='catalogos/headers/')
    footer_img = models.ImageField("Banner Inferior", upload_to='catalogos/footers/')
    fondo_color = models.CharField("Color de Fondo (Hex)", max_length=7, default="#FFFFFF")
    productos = models.ManyToManyField(Producto, related_name="catalogos", verbose_name="Productos a incluir")

    def __str__(self):
        return self.titulo