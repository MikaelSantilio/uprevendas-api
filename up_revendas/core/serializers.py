from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import serializers

from up_revendas.cars.models import Car
from up_revendas.cars.serializers import CarSerializer
from up_revendas.core.models import BankAccount, Customer, Purchase, Sale

User = get_user_model()


class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = ('id', 'bank', 'agency', 'account_type', 'name', 'cpf', 'balance')


class BankAccountHyperlinkSerializer(serializers.ModelSerializer):

    detail = serializers.HyperlinkedIdentityField(
        read_only=True,
        view_name='api:core:bank-account-detail', lookup_field='pk')

    class Meta:
        model = BankAccount
        fields = ('id', 'bank', 'balance', 'detail')


class PurchaseCreateSerializer(serializers.Serializer):
    car = CarSerializer()
    provider = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), required=True)
    buyer_for = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(
        Q(is_store_manager=True)), required=True)
    value = serializers.FloatField(required=True),
    bank_account = serializers.PrimaryKeyRelatedField(queryset=BankAccount.objects.all(), required=True)


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ('car', 'provider', 'buyer_for', 'value', 'bank_account')


class PurchaseHyperLinkSerializer(serializers.ModelSerializer):

    # license_plate = serializers.CharField(source='car.license_plate')
    detail = serializers.HyperlinkedIdentityField(
        read_only=True,
        view_name='api:comprar-detail', lookup_field='pk')

    class Meta:
        model = Purchase
        fields = ('created_at', 'value', 'detail')


class SaleSerializer(serializers.ModelSerializer):

    car = serializers.PrimaryKeyRelatedField(queryset=Car.objects.filter(sold=False), required=True)
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), required=True)
    seller = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(
        Q(is_employee=True) | Q(is_store_manager=True)), required=True)
    value = serializers.FloatField(required=True)
    bank_account = serializers.PrimaryKeyRelatedField(queryset=BankAccount.objects.all(), required=True)

    class Meta:
        model = Sale
        fields = ('car', 'customer', 'seller', 'value', 'bank_account')


class SaleHyperLinkSerializer(serializers.ModelSerializer):

    # license_plate = serializers.CharField(source='car.license_plate')
    detail = serializers.HyperlinkedIdentityField(
        read_only=True,
        view_name='api:vender-detail', lookup_field='pk')

    class Meta:
        model = Sale
        fields = ('created_at', 'value', 'detail')
