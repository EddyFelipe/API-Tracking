""" Users views """

# Django REST framework
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

# Permissions
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated

# Model
from api.models.users import User

# Serializers
from api.serializers.users import ( UserModelSerializer, 
                                    UserReadSerializer,
                                    UserLoginSerializer)

class UserViewSet( viewsets.ModelViewSet ):

    queryset = User.objects.filter(is_active=True)
    serializer_class = UserModelSerializer
    lookup_field = ('username')

    def get_serializer_class(self):

        # if self.action in ['list','retrieve','partial_update']:

        if self.action == 'create':
            return UserModelSerializer

        return UserReadSerializer
        
    
    def get_permissions(self):

        if self.action == 'login':
            permission = [AllowAny]
        else:
            permission = [IsAdminUser]

        return [p() for p in permission]
    
    def perform_destroy(self,user):
        """ Desactiva al usario, ya no prodrá mostrarse """
        user.is_active = False
        user.save()
    
   

    # Obtención de token
    @action(detail=False, methods=['post'])
    def login(self, request, *args, **kwargs ):

        serializer = UserLoginSerializer(data= request.data )
        if not serializer.is_valid():
            return Response({
                'err':{
                    'message':serializer.errors
                }
            }, status= status.HTTP_400_BAD_REQUEST )

        try:
            user = User.objects.get(username=serializer.data['username'], is_active=True)

            if user.check_password( serializer.data['password'] ):
                token, _ = Token.objects.get_or_create(user=user)

                return Response({
                    'usuario': UserReadSerializer(user).data,
                    'token': token.key
                }, status=status.HTTP_200_OK)

            return Response({
                'err':{
                    'message':'Usuario y contraseña incorrecto'
                }
            }, status= status.HTTP_400_BAD_REQUEST )
        
        except User.DoesNotExist:
            return Response({
                'err':{
                    'message':'Usuario no encontrado'
                }
            }, status= status.HTTP_400_BAD_REQUEST )
    
    @action(detail=False,methods=['get'])
    def admins(self, request, *args, **kwargs):
        """ Regresa el listado de los administradores """
        admins = User.objects.filter(is_staff=True, is_active=True)
        serializer = self.get_serializer(admins, many=True)
    
        return Response(serializer.data, status=status.HTTP_200_OK )

    @action(detail=False,methods=['get'])
    def clients(self, request, *args, **kwargs):
        """ Regresa el listado de los clientes """
        clients = User.objects.filter(is_client=True, is_active=True)
        serializer = self.get_serializer(clients, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK )
