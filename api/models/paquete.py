""" Paquete model """

# Django 
from django.db import models

class Paquete( models.Model ):

    codigo       = models.CharField( max_length=10, unique=True, blank=False )
    nombre       = models.CharField( max_length=30, blank=False )
    destinatario = models.CharField( max_length=64, blank=False )
    ubicacion    = models.CharField( max_length=64, blank=True )

    cliente       = models.ForeignKey('User', on_delete=models.CASCADE)

    # bodega    = 0
    # transito  = 1
    # entragado = 2

    ESTADOS = [
        (0,'En bodega'),
        (1,'En tránsito'),
        (2,'Entregado')
    ]

    estado        = models.PositiveSmallIntegerField(choices=ESTADOS, blank=False )
    creado_en     = models.DateTimeField(auto_now_add=True)
    modificado_en = models.DateTimeField(auto_now=True)
    eliminado     = models.BooleanField(default=False)

    class Meta:
        ordering = ['-modificado_en']