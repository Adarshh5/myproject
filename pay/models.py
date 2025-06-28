from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User


class UserAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=20, null=True, blank=True)
    Account_number = models.CharField(max_length = 12, unique=True, db_index=True)
    Phone_number = models.CharField(max_length = 10, db_index=True, unique=True, )
    upi_id = models.CharField(max_length = 15, unique=True, db_index=True)
    Password = models.CharField(max_length=6)
    Amount = models.DecimalField(max_digits=10, decimal_places=2, default=10000.00)



class BaseTransaction(models.Model):
    transaction_id = models.CharField(max_length=20, unique=True)
    account = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)


class TransactionHistory(BaseTransaction):
    recipient = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    name = models.CharField(max_length=50, null=True) 
    payment_method = models.CharField(max_length=10, choices=[
        ('upi', 'UPI ID'),
        ('account', 'Account Number'),
        ('phone', 'Phone Number'),
    ])



class MobileRechargeHistory(BaseTransaction):
    mobile_number = models.CharField(max_length=10)
    plan = models.CharField(max_length=10, choices=[
        ('199', 'Plan 1: ₹199 (1GB/day)'),
        ('399', 'Plan 2: ₹399 (2GB/day)'),
        ('599', 'Plan 3: ₹599 (3GB/day)'),
    ])

