from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_customer = models.BooleanField(default=False) #type: ignore

class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)



