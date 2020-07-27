
""" Model usuario """

from django.contrib.auth.models import AbstractUser

from django.db import models

class User( AbstractUser ):

    is_client    = models.BooleanField( default=False )
    phone_number = models.CharField( max_length=14, blank=True )

    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)
         