from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    fullname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'fullname']
