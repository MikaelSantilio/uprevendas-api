from django.contrib.auth import get_user_model
from django.db.models import Q
from django.urls import reverse
from rest_framework import serializers

from up_revendas.cars.models import Car
from up_revendas.cars.serializers import CarSerializer
from up_revendas.core.models import BankAccount, Customer, Purchase, Sale

User = get_user_model()


class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = ('id', 'bank', 'agency', 'account_type', 'name', 'cpf', 'balance')


class BankAccountHATEOASerializer(serializers.ModelSerializer):

    links = serializers.SerializerMethodField()

    class Meta:
        model = BankAccount
        fields = ('id', 'bank', 'balance', 'links')

    def get_links(self, obj):
        data = []

        request = self.context['request']

        if request.user.is_authenticated:

            if request.user.is_store_manager or request.user.is_superuser or request.user.is_employee:

                data += [
                    {
                        "type": "GET",
                        "rel": "self",
                        "uri": request.build_absolute_uri(
                            reverse("api:core:bank-account-detail", kwargs={'pk': obj.id}))
                    },
                    {
                        "type": "GET",
                        "rel": "conta_compras",
                        "uri": request.build_absolute_uri(
                            f'{reverse("api:core:purchase-list")}?bank_account={obj.id}')
                    },
                    {
                        "type": "GET",
                        "rel": "conta_vendas",
                        "uri": request.build_absolute_uri(
                            f'{reverse("api:core:sale-list")}?bank_account={obj.id}')
                    }
                ]

            if request.user.is_store_manager or request.user.is_superuser:
                data += [
                    {
                        "type": "PUT",
                        "rel": "conta_atualizacao",
                        "uri": request.build_absolute_uri(reverse("api:core:bank-account-detail", kwargs={'pk': obj.id}))
                    },
                    {
                        "type": "DELETE",
                        "rel": "conta_exclusao",
                        "uri": request.build_absolute_uri(reverse("api:core:bank-account-detail", kwargs={'pk': obj.id}))
                    }
                ]

        return data


class PurchaseCreateSerializer(serializers.Serializer):
    car = CarSerializer()
    provider = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), required=True)
    buyer_for = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(
        Q(is_store_manager=True)), required=True)
    value = serializers.FloatField(required=True)
    bank_account = serializers.PrimaryKeyRelatedField(queryset=BankAccount.objects.all(), required=True)


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ('car', 'provider', 'buyer_for', 'value', 'bank_account')


class PurchaseHATEOASerializer(serializers.ModelSerializer):

    links = serializers.SerializerMethodField()

    class Meta:
        model = Purchase
        fields = ('created_at', 'value', 'links')

    def get_links(self, obj):
        data = []

        request = self.context['request']

        if request.user.is_authenticated and (
                request.user.is_store_manager or request.user.is_superuser or request.user.is_employee):

            data.append(
                {
                    "type": "GET",
                    "rel": "self",
                    "uri": request.build_absolute_uri(
                        reverse("api:core:purchase-detail", kwargs={'pk': obj.id}))
                }
            )

        return data


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


class SaleHATEOASerializer(serializers.ModelSerializer):

    links = serializers.SerializerMethodField()

    class Meta:
        model = Sale
        fields = ('created_at', 'value', 'links')

    def get_links(self, obj):
        data = []

        request = self.context['request']

        if request.user.is_authenticated and (
                request.user.is_store_manager or request.user.is_superuser or request.user.is_employee):

            data += [
                {
                    "type": "GET",
                    "rel": "self",
                    "uri": request.build_absolute_uri(
                        reverse("api:core:sale-detail", kwargs={'pk': obj.id}))
                }
            ]

        return data
