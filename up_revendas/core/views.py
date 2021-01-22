from rest_framework import status
from django.db import transaction
from django.db import DatabaseError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from up_revendas.core.serializers import PurchaseCreateSerializer, PurchaseSerializer, SaleSerializer
from up_revendas.cars.serializers import CarSerializer


class BankAccountAPIView()

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
        PurchaseSerializer(data).save()


class SaleAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = SaleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response({'detail': 'Venda registrada com sucesso'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
