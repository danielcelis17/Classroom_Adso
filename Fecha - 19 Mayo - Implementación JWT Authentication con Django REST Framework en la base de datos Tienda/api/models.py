from django.db import models
from django.utils import timezone

# Las tablas las crea db/tienda_db.sql, no las migraciones de Django


class Cliente(models.Model):
    TIPOS_DOCUMENTO = [
        ('CC', 'Cédula de ciudadanía'),
        ('NIT', 'NIT'),
        ('CE', 'Cédula de extranjería'),
        ('PP', 'Pasaporte'),
    ]

    cliente_id = models.AutoField(primary_key=True)
    tipo_documento = models.CharField(max_length=3, choices=TIPOS_DOCUMENTO, default='CC')
    numero_documento = models.CharField(max_length=15, unique=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    telefono = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True, null=True, blank=True)
    direccion = models.CharField(max_length=150, null=True, blank=True)
    ciudad = models.CharField(max_length=50, default='Bogotá', null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'clientes'
        managed = False

    def __str__(self):
        return f'{self.nombre} {self.apellido}'


class Producto(models.Model):
    producto_id = models.AutoField(primary_key=True)
    nombre_producto = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.IntegerField(default=0)
    iva_porcentaje = models.DecimalField(max_digits=4, decimal_places=2, default=19.00, null=True, blank=True)

    class Meta:
        db_table = 'productos'
        managed = False

    def __str__(self):
        return self.nombre_producto


class Factura(models.Model):
    METODOS_PAGO = [
        ('Efectivo', 'Efectivo'),
        ('Tarjeta', 'Tarjeta'),
        ('Transferencia', 'Transferencia'),
        ('Nequi/Daviplata', 'Nequi/Daviplata'),
    ]

    factura_id = models.AutoField(primary_key=True)
    numero_factura = models.CharField(max_length=20, unique=True)
    fecha_emision = models.DateTimeField(default=timezone.now)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, db_column='cliente_id')
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    total_iva = models.DecimalField(max_digits=12, decimal_places=2)
    total_pagar = models.DecimalField(max_digits=12, decimal_places=2)
    metodo_pago = models.CharField(max_length=15, choices=METODOS_PAGO, default='Efectivo')

    class Meta:
        db_table = 'facturas'
        managed = False

    def __str__(self):
        return self.numero_factura


class DetalleFactura(models.Model):
    detalle_id = models.AutoField(primary_key=True)
    factura = models.ForeignKey(
        Factura, on_delete=models.CASCADE, db_column='factura_id', related_name='detalles'
    )
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, db_column='producto_id')
    cantidad = models.IntegerField()
    precio_venta = models.DecimalField(max_digits=12, decimal_places=2)
    subtotal_linea = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = 'detalle_facturas'
        managed = False

    def __str__(self):
        return f'{self.factura} - {self.producto}'
