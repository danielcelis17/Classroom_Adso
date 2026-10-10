from django.db import models


class Cliente(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido1 = models.CharField(max_length=100)
    # En ventas_db.sql estas columnas admiten NULL (ej. clientes 3, 4 y 7)
    apellido2 = models.CharField(max_length=100, null=True, blank=True)
    ciudad = models.CharField(max_length=100, null=True, blank=True)
    categoria = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'cliente'
        # La tabla la crea db/ventas_db.sql, no las migraciones de Django
        managed = False

    def __str__(self):
        return f'{self.nombre} {self.apellido1}'
