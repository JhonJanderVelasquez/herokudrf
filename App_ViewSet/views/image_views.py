from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

# Trae el serializador para producto
from App_ViewSet.serializers.general_serializers import ImageSerializer


class ImageViewSet(viewsets.ModelViewSet):
    serializer_class = ImageSerializer

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
            return Response({'message': 'Imagen creada exitosamente'}, status= status.HTTP_201_CREATED)
        return Response (serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    # Actualizar registro de imagen
    def update (self, request, pk=None):
        if self.get_queryset(pk):
            Image_serializer = self.serializer_class(self.get_queryset(pk), data=request.data)
            if Image_serializer.is_valid():
                Image_serializer.save()
                return Response({
                    "message": "Imagen actualizada", 
                    'response': Image_serializer.data
            }, status=status.HTTP_200_OK)
        return Response({'error':'No existe una imagen con estos datos!'}, status=status.HTTP_400_BAD_REQUEST)

    # Este método sobreescribe el delete, no es necesario porque la clase lo ejecuta por default, 
    # pero es para tener un mayor control. 
    def destroy (self, request, pk=None):
        image = self.get_queryset().filter(id=pk).first()
        if image:
            image.delete()
            return Response({'message':'Imagen eliminada exitosamente'}, status=status.HTTP_200_OK)
        return Response({'error': 'No existe una imagen con estos datos...'}, status=status.HTTP_400_BAD_REQUEST)