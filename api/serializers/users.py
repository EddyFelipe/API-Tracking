""" Serializer de users """

# django REST framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

# Django hashes
from django.contrib.auth.hashers import make_password

# Model
from api.models.users import User

class UserModelSerializer( serializers.ModelSerializer ):

    email = serializers.CharField(
        required=True, 
        validators=[ UniqueValidator( queryset=User.objects.all(), message='El email debe ser único' ) ]
    )
    username = serializers.CharField(validators=[ UniqueValidator( queryset=User.objects.all(), message='El username debe ser único')])
    first_name = serializers.CharField(required=True)
    last_name  = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            'id',
            'first_name','last_name','phone_number',
            'email','username', 'password',
            'is_staff','is_client'
            )
        # exclude = ['password']
    
    def validate( self, data ):

        is_staff = data.get('is_staff', None)
        is_client = data.get('is_client', None)

        igual = ( bool(is_client) == bool(is_staff) ) if True else False

        if igual:
            raise serializers.ValidationError('El role del usuario (is_staff or is_client)')
        return data
    
    def create(self, validated_data ):
        """ Encriptar la contraseña del usuario"""
        validated_data['password'] = make_password( validated_data.get('password') )
        return User.objects.create(**validated_data)

class UserReadSerializer( serializers.ModelSerializer ):
    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'username', 
            'phone_number',
            'is_active',
            'is_staff',
            'is_client'
        )

# Inicio de Sesión
class UserLoginSerializer( serializers.Serializer ):

    password  = serializers.CharField(required=True, max_length=64)
    username = serializers.CharField(required=True, max_length=20)