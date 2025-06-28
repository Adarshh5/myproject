from django.db import models
from pay.models import UserAccount
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class PrivateToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Linkend_account =  models.OneToOneField(UserAccount, on_delete=models.CASCADE)
    token = models.CharField(max_length=10, unique=True)



class SaveData(models.Model):
     upi_id = models.CharField(max_length = 15)
     PojectIdentity = models.CharField(max_length=10)
     name = models.CharField(max_length = 15)
     amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
     IdentityOfUser =  models.CharField(max_length=10)
     payment_mode = models.CharField(
        max_length=8,
        choices=[('Active', 'Active'), ('Deactive', 'Deactive')],
        default='Active'
    )




