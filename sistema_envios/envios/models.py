# pylint: disable=no-member

from django.db import models
from django.utils import timezone

class Usuario(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.nombre}"
      

       


class Transaccion(models.Model):
    TIPO_CHOICES = [
        ('envio', 'Envío de Dinero'),
        ('deposito', 'Depósito'),
        ('retiro', 'Retiro'),
        ('pago', 'Pago de Servicio'),
    ]
    usuario = models.ForeignKey(Usuario, related_name='transacciones', on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField(blank=True)
    fecha = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.usuario.nombre} - {self.tipo} - ${self.monto}".strip()
