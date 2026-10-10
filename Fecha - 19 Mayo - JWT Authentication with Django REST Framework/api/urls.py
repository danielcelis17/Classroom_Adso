from rest_framework.routers import DefaultRouter
from .views import ClienteViewSet, ComercialViewSet, PedidoViewSet

app_name = 'api'

# Sin barra final para conservar la ruta /api/cliente de la fase 1
router = DefaultRouter(trailing_slash=False)
router.register('cliente', ClienteViewSet)
router.register('comercial', ComercialViewSet)
router.register('pedido', PedidoViewSet)

urlpatterns = router.urls
