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
    BankAccountHyperlinkSerializer,
    BankAccountSerializer,
    PurchaseCreateSerializer,
    PurchaseHyperLinkSerializer,
    PurchaseSerializer,
    SaleHyperLinkSerializer,
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
        return self.custom_paginated_queryset(request, BankAccountHyperlinkSerializer)


class PurchaseViewSet(ListPaginatedMixin, viewsets.ViewSet):
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
        return self.custom_paginated_queryset(request, PurchaseHyperLinkSerializer)

    def create(self, request):
        serializer = PurchaseCreateSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            self.save_data(data)

            return Response({'detail': 'Compra registrada com sucesso'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        purchase = get_object_or_404(Purchase, pk=pk)
        serializer = PurchaseSerializer(purchase)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def save_data(self, data):

        car = CarSerializer(data=data['car']).save()
        data['car'] = car.id

        customer = get_object_or_404(Customer, id=data['provider'])

        bank_account = get_object_or_404(BankAccount, id=data['bank_account'])

        if bank_account.balance < data['value']:
            raise HttpResponseBadRequest(message='Conta bancária com fundos insuficientes!')

        bank_account.balance -= data['value']
        customer.balance += data['value']

        serializer = PurchaseSerializer(data)
        serializer.save()
        bank_account.save()
        customer.save()


class SaleViewSet(ListPaginatedMixin, viewsets.ViewSet):
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
        return self.custom_paginated_queryset(request, SaleHyperLinkSerializer)

    def create(self, request):
        serializer = SaleSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            self.save_data(data)

            return Response({'detail': 'Venda registrada com sucesso'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        sale = get_object_or_404(Sale, pk=pk)
        serializer = SaleSerializer(sale)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def save_data(self, data):

        car = get_object_or_404(Car, id=data['car'])
        customer = get_object_or_404(Customer, id=data['customer'])
        bank_account = get_object_or_404(BankAccount, id=data['bank_account'])

        if customer.balance < data['value']:
            raise HttpResponseBadRequest(message='Cliente com fundos insuficientes!')

        elif data['value'] < car.min_sale_value:
            raise HttpResponseBadRequest(
                message=f'Carro não pode ser vendido abaixo do valor minimo de R$ {car.min_sale_value:.2f}!')

        elif car.sold is True:
            raise HttpResponseBadRequest(message='Carro não disponível para venda!')

        customer.balance -= data['value']
        bank_account.balance += data['value']
        car.sold = True

        serializer = SaleSerializer(data=data)
        serializer.save()
        bank_account.save()
        customer.save()
        car.save()
