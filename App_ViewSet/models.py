from django.db import models

class Producto (models.Model):
    nombre = models.CharField('Nombre del producto', max_length=100, unique=True)
    descripcion = models.TextField('Descripción del producto', max_length=150)
    precio = models.IntegerField('Precio')
    iva = models.IntegerField('Iva')                 
    marca = models.CharField('Marca', max_length=25, blank=True, ) 

    class Meta:
        verbose_name="Producto"
        verbose_name_plural="Productos"

    def __str__(self):
        return self.nombre


class Imagen (models.Model):
    url = models.CharField('Url de la imagen', max_length=150, blank=True, null=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name='Producto')

    class Meta:
        verbose_name="Imagen"
        verbose_name_plural="Imágenes"