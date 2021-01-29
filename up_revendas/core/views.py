from django.db import transaction
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from up_revendas.cars.models import Car
from up_revendas.cars.serializers import CarSerializer
from up_revendas.core.models import BankAccount, Customer, Purchase, Sale
from up_revendas.core.permissions import IsEmployee, IsStoreManager
from up_revendas.core.serializers import (
    BankAccountHATEOASerializer,
    BankAccountSerializer,
    PurchaseCreateSerializer,
    PurchaseHATEOASerializer,
    PurchaseSerializer,
    SaleHATEOASerializer,
    SaleSerializer,
)


class ListPaginatedMixin():

    def custom_paginated_queryset(self, request, Serializer):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = Serializer(page, many=True, context={"request": request})
            return self.get_paginated_response(serializer.data)

        serializer = Serializer(queryset, many=True, context={"request": request})
        return Response(serializer.data)


class BankAccountViewSet(ListPaginatedMixin, viewsets.ModelViewSet):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['bank']
    ordering_fields = ['balance']

    def get_permissions(self):

        if self.action == 'list':
            permission_classes = [IsAdminUser | IsStoreManager | IsEmployee]
        elif self.action == 'retrieve':
            permission_classes = [IsAdminUser | IsStoreManager | IsEmployee]
        else:
            permission_classes = [IsAdminUser | IsStoreManager]
        return [permission() for permission in permission_classes]

    def list(self, request):
        return self.custom_paginated_queryset(request, BankAccountHATEOASerializer)


class PurchaseViewSet(ListPaginatedMixin, viewsets.GenericViewSet):
    queryset = Purchase.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['provider', 'car', 'buyer_for', 'bank_account']
    ordering_fields = ['value', 'created_at', 'updated_at']

    def get_permissions(self):

        if self.action == 'list':
            permission_classes = [IsAdminUser | IsStoreManager | IsEmployee]
        elif self.action == 'retrieve':
            permission_classes = [IsAdminUser | IsStoreManager | IsEmployee]
        else:
            permission_classes = [IsAdminUser | IsStoreManager]
        return [permission() for permission in permission_classes]

    def list(self, request):
        return self.custom_paginated_queryset(request, PurchaseHATEOASerializer)

    def create(self, request):
        serializer = PurchaseCreateSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data

            response = self.save_data(data)
            if response[0] is True:
                return Response(response[1], status=status.HTTP_200_OK)
            else:
                return Response(response[1], status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        purchase = get_object_or_404(Purchase, pk=pk)
        serializer = PurchaseSerializer(purchase)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def save_data(self, data):

        if data['car']['min_sale_value'] < data['value']:
            return [False, {'detail': 'Valor mínimo de venda deve ser maior ou igual ao valor de compra.'}]

        car_serializer = CarSerializer(data=data['car'])

        if not car_serializer.is_valid():
            return [False, car_serializer.errors]

        car = car_serializer.save()
        data['car'] = car.id

        customer = get_object_or_404(Customer, pk=data['provider'])
        bank_account = get_object_or_404(BankAccount, pk=data['bank_account'])

        if bank_account.balance < data['value']:
            return [False, {'detail': 'Conta bancária com fundos insuficientes!'}]

        bank_account.balance -= data['value']
        customer.balance += data['value']

        serializer = PurchaseSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            bank_account.save()
            customer.save()
            return [True, {'detail': 'Compra registrada com sucesso'}]
        return [False, serializer.errors]


class SaleViewSet(ListPaginatedMixin, viewsets.GenericViewSet):
    queryset = Sale.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['customer', 'car', 'seller', 'bank_account']
    ordering_fields = ['value', 'created_at', 'updated_at']

    def get_permissions(self):

        if self.action == 'list':
            permission_classes = [IsAdminUser | IsStoreManager | IsEmployee]
        elif self.action == 'retrieve':
            permission_classes = [IsAdminUser | IsStoreManager | IsEmployee]
        else:
            permission_classes = [IsAdminUser | IsStoreManager]
        return [permission() for permission in permission_classes]

    def list(self, request):
        return self.custom_paginated_queryset(request, SaleHATEOASerializer)

    def create(self, request):
        serializer = SaleSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            response = self.save_data(data)
            if response[0] is True:
                return Response(response[1], status=status.HTTP_200_OK)
            else:
                return Response(response[1], status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        sale = get_object_or_404(Sale, pk=pk)
        serializer = SaleSerializer(sale)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def save_data(self, data):

        car = get_object_or_404(Car, pk=data['car'])
        customer = get_object_or_404(Customer, pk=data['customer'])
        bank_account = get_object_or_404(BankAccount, pk=data['bank_account'])

        if customer.balance < data['value']:
            return [False, {'detail': 'Cliente com fundos insuficientes!'}]

        elif data['value'] < car.min_sale_value:
            return [False,
                    {'detail': f'Carro não pode ser vendido abaixo do valor minimo de R$ {car.min_sale_value:.2f}!'}]

        elif car.sold is True:
            return [False, {'detail': 'Carro não disponível para venda!'}]

        customer.balance -= data['value']
        bank_account.balance += data['value']
        car.sold = True

        serializer = SaleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            bank_account.save()
            customer.save()
            car.save()
            return [True, {'detail': 'Venda registrada com sucesso'}]
        return [False, serializer.errors]
