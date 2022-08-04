#### Toda esta documentación está pensada para realizarse de forma local en cada computador usando Visual Studio Code.

# 1. CONFIGURACIÓN INICIAL
Rest API construída con el framework de Django y con vistas ViewSets. 

1. Clonar este respositorio
```
https://github.com/JhonJanderVelasquez/Rest_API_ViewSet_Entrevista.git
```

2. Crear entorno Virtual 
```
virtualenv env
```

3. Activar entorno Virtual

4. Instalar librerías
```
(env) pip install -r requirements.txt 
```

5. Iniciar servidor local
```
(env) python manage.py runserver 
```

6. Puedes crear y obtener una lista de todos los productos con la siguiente url. 
Puedes realizar las operaciones GET y POST con POSTMAN o con la interfaz de Django Framework.
```
http://localhost:8000/api/products/
```

7. Para eliminar, actualizar y obtener el detalle de un producto, utilizas la siguiente url indicando el id del producto.
```
http://localhost:8000/api/products/{id}
```

![image](https://user-images.githubusercontent.com/110197737/182057534-f15a7fbd-7d21-436a-9eb6-60b7c636f4f7.png)

Como se ve en la imagen de arriba de las urls de esta API, para realizar las operaciones CRUD con el Modelo Imágenes, se realiza de la misma manera que con productos.


# 2. DOCUMENTACIÓN SWAGGER.
### Conociendo más sobre la API:

La documentación de todas las rutas de acceso para la API están registradas y personalizadas en la siguiente ruta.
```
http://localhost:8000/swagger/
```

Como se podrá observar en el siguiente pantallazo, en color rojo está la url, en color verde están los padres de las rutas. 
Dentro de las rutas están cada uno de los métodos HTTP y cómo ejecutarlas. 
Finalmente también se puede observar en azul los modelos de la API y sus campos.

![image](https://user-images.githubusercontent.com/110197737/182061840-f1e5969f-8790-48a8-9c6f-031d28606db9.png)



# 3. BREVE ACERCAMIENTO AL CÓDIGO.

1. El modelo para Productos se puede ver a continuación.

```python
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
```

2. El modelo de las imágenes se muestra a continuación. Producto es una llave foránea. La url puede estar vacía.

```python
class Imagen (models.Model):
    url = models.CharField('Url de la imagen', max_length=150, blank=True, null=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name='Producto')

    class Meta:
        verbose_name="Imagen"
        verbose_name_plural="Imágenes"
```

3. Estos son los serializadores de las clases ViewSets, que realizan las conversiones a JSON, compara los datos y realiza las validaciones.
para este caso específico se obtienen todos los campos. Para el serializador de las imágenes se utiliza el método To_Representation para retornar
los campos que se deseen, lo mismo para los datos que contiene la llave foránea.

```python
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
```

4. Las clases para los ViewSets se programaron sobre-escribiendo los métodos list, create, update, destroy... Este es el ViewSet del Producto, 
pero es lo mismo para las imágenes.
```python
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

# Trae el serializador para producto
from API.serializers.general_serializers import ProductSerializer

# Crear y listar productos
class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter()
        else:
            return self.get_serializer().Meta.model.objects.filter(id = pk).first()

    # Sobreescribiendo método post de la clase
    def create (self, request): 
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response ({'message': 'Producto creado exitosamente'}, status= status.HTTP_201_CREATED)
        return Response (serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    # Actualiza registro con un id ingresado por url.
    def update (self, request, pk=None):
        if self.get_queryset(pk):
            product_serializer = self.serializer_class(self.get_queryset(pk), data=request.data)
            if product_serializer.is_valid():
                product_serializer.save()
                return Response({
                    "message": "Producto actualizado", 
                    'response': product_serializer.data
                }, status=status.HTTP_200_OK)
        return Response({'error':'No existe un producto con estos datos!'}, status=status.HTTP_400_BAD_REQUEST)

    # Este método sobreescribe el delete, no es necesario, pero se puede tener un mayor control. 
    def destroy (self, request, pk=None):
        product = self.get_queryset().filter(id=pk).first()
        if product:
            product.delete()
            return Response({'message':'Producto eliminado exitosamente'}, status=status.HTTP_200_OK)
        return Response({'error': 'No existe un producto con estos datos...'}, status=status.HTTP_400_BAD_REQUEST)
```

# 4. ENRUTADOR.

Las rutas para el enrutador están configuradas de la siguiente manera.

```python
from rest_framework.routers import DefaultRouter
from API.views.product_views import ProductViewSet
from API.views.image_views import ImageViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='products')
router.register(r'images', ImageViewSet, basename='images')

urlpatterns = router.urls
```
