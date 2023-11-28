from rest_framework import serializers


class PaymentSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20)
    amount = serializers.IntegerField()
