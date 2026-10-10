from django.contrib import admin
from .models import Cliente, Comercial, Pedido

admin.site.register(Cliente)
admin.site.register(Comercial)
admin.site.register(Pedido)
