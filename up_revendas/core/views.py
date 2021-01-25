from django.db import transaction
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from up_revendas.cars.models import Car
from up_revendas.cars.serializers import CarSerializer
from up_revendas.core.models import BankAccount, Customer
from up_revendas.core.permissions import IsEmployee, IsStoreManager
from up_revendas.core.serializers import (
    BankAccountSerializer,
    PurchaseCreateSerializer,
    PurchaseSerializer,
    SaleSerializer,
    BankAccountHyperlinkSerializer
)


class BankAccountListCreateAPIView(ListCreateAPIView):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer
    permission_classes = [IsAdminUser | IsStoreManager | IsEmployee]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = BankAccountHyperlinkSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = BankAccountHyperlinkSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)


class BankAccountRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer
    permission_classes = [IsAdminUser | IsStoreManager]


class PurchaseAPIView(APIView):

    permission_classes = [IsAdminUser | IsStoreManager]

    def post(self, request, format=None):
        serializer = PurchaseCreateSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            self.save_data(data)

            return Response({'detail': 'Compra registrada com sucesso'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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


class SaleAPIView(APIView):

    permission_classes = [IsAdminUser | IsStoreManager | IsEmployee]

    def post(self, request, format=None):
        serializer = SaleSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            self.save_data(data)

            return Response({'detail': 'Venda registrada com sucesso'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
