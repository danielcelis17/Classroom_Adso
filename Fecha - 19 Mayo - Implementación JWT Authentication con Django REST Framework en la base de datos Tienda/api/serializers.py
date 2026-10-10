from rest_framework import serializers
from .models import Cliente, Producto, Factura, DetalleFactura


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'


class DetalleFacturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleFactura
        fields = '__all__'


class FacturaSerializer(serializers.ModelSerializer):
    # Las líneas se crean en /detalle-facturas; aquí solo se muestran
    detalles = DetalleFacturaSerializer(many=True, read_only=True)

    class Meta:
        model = Factura
        fields = '__all__'
