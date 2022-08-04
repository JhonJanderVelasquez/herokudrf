from rest_framework.routers import DefaultRouter
from App_ViewSet.views.product_views import ProductViewSet
from App_ViewSet.views.image_views import ImageViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='products')
router.register(r'images', ImageViewSet, basename='images')

urlpatterns = router.urls