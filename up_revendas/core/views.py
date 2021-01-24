from django.db import DatabaseError, transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.forms import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from up_revendas.cars.serializers import CarSerializer
from up_revendas.cars.models import Car
from up_revendas.core.models import BankAccount
from up_revendas.core.permissions import IsStoreManager
from up_revendas.core.serializers import (
    BankAccountSerializer,
    PurchaseCreateSerializer,
    PurchaseSerializer,
    SaleSerializer,
)


class BankAccountListCreateAPIView(ListCreateAPIView):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer
    permission_classes = [IsAdminUser, IsStoreManager]


class BankAccountRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer
    permission_classes = [IsAdminUser, IsStoreManager]


class PurchaseAPIView(APIView):

    permission_classes = [AllowAny]

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
        customer = Customer.objects.get(id=data['provider'])
        id_bank_account = data['bank_account']
        bank_account = get_object_or_404(BankAccount, id=id_bank_account)
        if bank_account.balance < data['value']:
            raise ValidationError(message='Conta bancária com fundos insuficientes!')

        else:
            bank_account.balance -= data['value']
            customer.balance += data['value']

        PurchaseSerializer(data).save()
        bank_account.save()


class SaleAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = SaleSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            car = Car.objects.get(id=data['car'])
            car.sold = True
            serializer.save()

            return Response({'detail': 'Venda registrada com sucesso'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @transaction.atomic
    def save_data(self, data):

        car = CarSerializer(data=data['car']).save()
        data['car'] = car.id
        customer = Customer.objects.get(id=data['customer'])
        id_bank_account = data['bank_account']
        bank_account = get_object_or_404(BankAccount, id=id_bank_account)
        if customer.balance < data['value']:
            raise ValidationError(message='Cliente com fundos insuficientes!')

        else:
            customer.balance -= data['value']
            bank_account.balance += data['value']

        PurchaseSerializer(data).save()
        bank_account.save()
        customer.save()