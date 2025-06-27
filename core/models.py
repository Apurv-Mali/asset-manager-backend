from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here

class User(AbstractUser):
    ROLE_CHOICES = [
        ('manager', 'Manager'),
        ('mechanic', 'Mechanic'),
    ]
    email = models.EmailField( null=True)
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    salary = models.IntegerField(null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, blank=True)