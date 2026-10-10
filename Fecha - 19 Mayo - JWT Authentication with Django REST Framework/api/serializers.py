from rest_framework import serializers
from .models import Cliente, Comercial, Pedido


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'


class ComercialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comercial
        fields = '__all__'


class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'
