from django.db import models

from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    nombre = models.CharField(max_length=50, null=True, blank=True) #Nombre del profesor
    apellido = models.CharField(max_length=100, null=True, blank=True) #Nombre del profesor