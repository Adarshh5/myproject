from django.contrib import admin
from .models import UserAccount, TransactionHistory, MobileRechargeHistory

@admin.register(UserAccount)
class UserAccountModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'Account_number', "Phone_number" ]


@admin.register(TransactionHistory)
class TransactionHistoryModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'recipient', 'account','amount']


@admin.register(MobileRechargeHistory)
class MobileRechargehistory(admin.ModelAdmin):
    list_display = ['id', 'account','plan']