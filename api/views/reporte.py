""" ViewSet reporte """

# Django REST framework
from rest_framework import viewsets,status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

# Model
from api.models.users import User
from api.models.paquete import Paquete

# Serializers 
from api.serializers.users import UserReadSerializer
from api.serializers.paquete import PaqueteRepSerializer, PaqueteReadSerializer


# ========================================================
#               REPORTE PARA EL CLIENTE 
# ========================================================
class ReporteClientViewSet( viewsets.ReadOnlyModelViewSet ):
    """ El cliente puede consultar los paquetes que tiene """

    serializer_class = PaqueteRepSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = ('codigo')

    def get_queryset(self):
        return Paquete.objects.filter(cliente=self.request.user)
    
    @action(detail=False, methods=['get'])
    def transito(self, request, *args, **kwargs ):
        return self.response_estado(1)
    
    @action(detail=False, methods=['get'])
    def bodega(self, request, *args, **kwargs ):
        return self.response_estado(0)
        

    def response_estado(self, estado):
        cliente = self.request.user
        try:
            paquetes   = Paquete.objects.filter(cliente=cliente, estado=estado)
            serializer = self.get_serializer(paquetes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Paquete.DoesNotExist:
            return Response({
                'err':{
                    'message': 'No existe ningún paquete'
                }
            }, status=status.HTTP_400_BAD_REQUEST)


# ========================================================
#               REPORTE PARA EL ADMINISTRADOR 
# ========================================================
class ReporteAdminntViewSet( viewsets.ReadOnlyModelViewSet ):
    
    serializer_class = PaqueteReadSerializer
    queryset = Paquete.objects.filter(eliminado=False)
    lookup_field = ('codigo')
    permission_classes = [IsAdminUser]

    # ============================================================
    # En la base de datos un número entero para designar el estado
    # Si el estado tiene 0 el paquete se encuentra en la bodega
    #  bodege = 0
    #  transito = 1
    #  entregado = 2
    # =============================================================
    @action(detail=False, methods=['get'])
    def bodega( self, request, *args, **kwargs ):
        return self.response_estado(0)

    @action(detail=False, methods=['get'])
    def transito( self, request, *args, **kwargs ):
        return self.response_estado(1)

    @action(detail=False, methods=['get'])
    def entregado( self, request, *args, **kwargs ):
        return self.response_estado(2)
        
    def response_estado(self, estado ):
        try:
            paquetes = Paquete.objects.filter(estado=estado,eliminado=False)
            page = self.paginate_queryset(paquetes)
            serializer = self.get_serializer(page, many=True)

            # return Response({
            #     'total':len(serializer.data),
            #     'paquetes': serializer.data
            # }, status=status.HTTP_200_OK)
            return self.get_paginated_response(serializer.data)

        except Paquete.DoesNotExist:
            return Response({
                'err':{
                    'message': 'No existe ningún paquete'
                }
            }, status=status.HTTP_400_BAD_REQUEST)