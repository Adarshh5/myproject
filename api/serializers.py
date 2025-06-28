from rest_framework import serializers


class PaybuddySerializer(serializers.Serializer):
    upi_id = serializers.CharField(max_length=100)
    PojectIdentity = serializers.CharField(max_length=10)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    name = serializers.CharField()
    IdentityOfUser = serializers.CharField()

