from django.contrib import admin
from App_ViewSet.models import *

class ImageAdmin (admin.ModelAdmin):
    list_display = ('id', 'producto')

class ProductAdmin (admin.ModelAdmin):
    list_display = ('id', 'nombre', 'precio')

admin.site.register(Producto, ProductAdmin)
admin.site.register(Imagen, ImageAdmin)