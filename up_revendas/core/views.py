from django.db import DatabaseError, transaction
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from up_revendas.cars.serializers import CarSerializer
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

    # def get(self, request, format=None):
    #     filters = request.query_params

    #     if ('week_day' not in filters or 'subject' not in filters or 'time' not in filters):
    #         return Response(
    #             {'error': 'Não há filtros para procurar aulas'},
    #             status=status.HTTP_400_BAD_REQUEST)

    #     qs_class_schedule = ClassSchedule.objects.filter(
    #         klass__subject=filters['subject'],
    #         week_day=filters['week_day'], start_at__lte=str_hour_to_minutes(filters['time']),
    #         end_at__gt=str_hour_to_minutes(filters['time']))

    #     data = []

    #     for class_schedule in qs_class_schedule:
    #         serializer = ClassScheduleSerializer(class_schedule)
    #         data.append(serializer.data['klass'])

    #     return Response(data, status=status.HTTP_200_OK)

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
        id_bank_account = data['bank_account']
        bank_account = get_object_or_404(BankAccount, id=id_bank_account)
        if bank_account.balance < data['value']:
            raise ValidationError()
        else:
            bank_account.balance -= data['value']

        PurchaseSerializer(data).save()


class SaleAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = SaleSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            serializer.save()

            return Response({'detail': 'Venda registrada com sucesso'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
