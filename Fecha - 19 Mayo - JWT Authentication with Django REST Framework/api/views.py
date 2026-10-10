from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import ClienteSerializer, ComercialSerializer, PedidoSerializer
from .models import Cliente, Comercial, Pedido


class ClienteViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = Cliente.objects.all().order_by('id')
    serializer_class = ClienteSerializer


class ComercialViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = Comercial.objects.all().order_by('id')
    serializer_class = ComercialSerializer


class PedidoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = Pedido.objects.all().order_by('id')
    serializer_class = PedidoSerializer
