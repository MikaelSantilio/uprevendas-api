from django.contrib.auth import get_user_model
from rest_framework import serializers

from up_revendas.cars.serializers import CarSerializer
from up_revendas.core.models import Customer, Purchase, Sale

User = get_user_model()


class PurchaseCreateSerializer(serializers.Serializer):
    car = CarSerializer()
    provider = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), required=True)
    buyer_for = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)
    value = serializers.FloatField(required=True)


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ('car', 'provider', 'buyer_for', 'value')


class SaleSerializer(serializers.ModelSerializer):

    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), required=True)
    seller = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)
    value = serializers.FloatField(required=True)

    class Meta:
        model = Sale
        fields = ('car', 'customer', 'seller', 'value')
