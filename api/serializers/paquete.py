""" Paquete serializers """

# Django REST framework
from rest_framework import serializers

# Model
from api.models import Paquete

# Utilidades
import random
from string import digits

class PaqueteModelSerializer( serializers.ModelSerializer ):

    codigo = serializers.CharField(required=False)

    class Meta:
        model = Paquete
        # fields = '__all__'
        exclude = ['id','eliminado']

    def validate(self, data ):
        """ Verifica si se asigno la ubicación cuando se 
            el estado del paquete se establece en transito
        """
        estado = data.get('estado')

        if estado == 1:
            ubicacion = data.get('ubicacion',None)
            if ubicacion is None:
                raise serializers.ValidationError('Es necesario especificar la ubicación')
        
        return data

    def create( self, data ):
        codigo = self.codigo_barra()

        # Verifica si el código generado no se ha asignado a un paquete
        while Paquete.objects.filter(codigo=codigo).exists():
            codigo = self.codigo_barra()
        
        data['codigo'] = codigo
        return Paquete.objects.create(**data)

    def codigo_barra(self):
        return ''.join( random.choices(digits,k=10) )

class PaqueteReadSerializer( serializers.ModelSerializer ):

    estado  = serializers.CharField(source='get_estado_display')
    cliente = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Paquete
        exclude = ['id','eliminado']

class PaqueteRepSerializer( serializers.ModelSerializer ):

    estado  = serializers.CharField(source='get_estado_display')

    class Meta:
        model = Paquete
        exclude = ['id','eliminado','cliente']
