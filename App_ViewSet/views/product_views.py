from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

# Trae el serializador para producto
from App_ViewSet.serializers.general_serializers import ProductSerializer

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
