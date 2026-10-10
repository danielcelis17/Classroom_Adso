from rest_framework.routers import DefaultRouter
from .views import ClienteViewSet, ProductoViewSet, FacturaViewSet, DetalleFacturaViewSet

app_name = 'api'

router = DefaultRouter(trailing_slash=False)
router.register('clientes', ClienteViewSet)
router.register('productos', ProductoViewSet)
router.register('facturas', FacturaViewSet)
router.register('detalle-facturas', DetalleFacturaViewSet)

urlpatterns = router.urls
