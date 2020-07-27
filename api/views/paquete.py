"""" Paquete views """

# django REST framework
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action

# Model
from api.models.paquete import Paquete

# Serializer
from api.serializers.paquete import (
                                    PaqueteModelSerializer,
                                    PaqueteReadSerializer
                                    )

class PaqueteViewSet( viewsets.ModelViewSet ):

    queryset = Paquete.objects.filter(eliminado=False)
    serializer_class = PaqueteModelSerializer
    permission_classes = [IsAdminUser]
    lookup_field = ('codigo')

    def get_serializer_class(self):

        if self.action in ['list','retrieve']:
            return PaqueteReadSerializer
        
        return PaqueteModelSerializer
    
    def perform_destroy(self, paquete ):
        paquete.eliminado = True
        paquete.save()
