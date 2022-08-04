from API.models import Producto, Imagen
from rest_framework import serializers

class ProductSerializer(serializers.ModelSerializer):
    # Trae el modelo y los campos que seleccionados
    class Meta:
        model = Producto
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imagen
        fields = '__all__'
    
    # Se escoge este método de representación de datos para mayor escalabilidad y control del proyecto.
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'url': instance.url,
            # Llave foránea
            'producto': {   
                "id": instance.producto.id,
                "nombre": instance.producto.nombre,
                "descripcion": instance.producto.descripcion,
                "precio": instance.producto.precio,
                "iva": instance.producto.iva,
                "marca": instance.producto.marca
            }
        }