from django.contrib.auth import get_user_model
from rest_framework import serializers

from up_revendas.cars.serializers import CarSerializer
from up_revendas.cars.models import Car
from up_revendas.core.models import Customer, Purchase, Sale, BankAccount

User = get_user_model()


class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = '__all__'


class PurchaseCreateSerializer(serializers.Serializer):
    car = CarSerializer()
    provider = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), required=True)
    buyer_for = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)
    value = serializers.FloatField(required=True),
    bank_account = serializers.PrimaryKeyRelatedField(queryset=BankAccount.objects.all(), required=True)


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ('car', 'provider', 'buyer_for', 'value', 'bank_account')


class SaleSerializer(serializers.ModelSerializer):

    car = serializers.PrimaryKeyRelatedField(queryset=Car.objects.filter(sold=False), required=True)
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), required=True)
    seller = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)
    value = serializers.FloatField(required=True)
    bank_account = serializers.PrimaryKeyRelatedField(queryset=BankAccount.objects.all(), required=True)

    class Meta:
        model = Sale
        fields = ('car', 'customer', 'seller', 'value', 'bank_account')
