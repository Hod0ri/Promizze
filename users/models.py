from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    id = models.CharField(max_length=500, primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None
    userRole = models.CharField(max_length=255, default='Guest')
    '''
    $ User Permission List
    Admin / PM / PL / PE / Guest
    '''

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
