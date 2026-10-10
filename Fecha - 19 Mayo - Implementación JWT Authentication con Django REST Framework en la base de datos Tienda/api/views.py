from django.db.models import ProtectedError
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import (
    ClienteSerializer, ProductoSerializer, FacturaSerializer, DetalleFacturaSerializer,
)
from .models import Cliente, Producto, Factura, DetalleFactura


class ProtegidoMixin:
    """Responde 409 en vez de 500 al borrar un registro que está en facturas."""

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            return Response(
                {'detail': 'No se puede eliminar: el registro está asociado a facturas.'},
                status=status.HTTP_409_CONFLICT,
            )


class ClienteViewSet(ProtegidoMixin, viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = Cliente.objects.all().order_by('cliente_id')
    serializer_class = ClienteSerializer


class ProductoViewSet(ProtegidoMixin, viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = Producto.objects.all().order_by('producto_id')
    serializer_class = ProductoSerializer


class FacturaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = Factura.objects.prefetch_related('detalles').order_by('factura_id')
    serializer_class = FacturaSerializer


class DetalleFacturaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = DetalleFactura.objects.all().order_by('detalle_id')
    serializer_class = DetalleFacturaSerializer
