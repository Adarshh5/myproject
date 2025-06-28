from django.contrib import admin
from api.models import PrivateToken, SaveData

@admin.register(PrivateToken)
class PrivateTokenModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'Linkend_account', "token" ]


@admin.register(SaveData)
class SaveDataModelAdmin(admin.ModelAdmin):
    list_display  =['id', 'name', 'PojectIdentity', 'amount', 'IdentityOfUser', 'upi_id']
