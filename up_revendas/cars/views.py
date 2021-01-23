from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny

from up_revendas.cars.models import Car
from up_revendas.cars.serializers import CarHyperlinkSerializer, CarSerializer


class CarHyperlinkListCreateAPIView(ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarHyperlinkSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['brand', 'model', 'car_type', 'color', 'transmission']
    ordering_fields = ['sale_value', 'mileage', 'year', 'version']
    # ordering = ['sale_value']


class CarRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [AllowAny]
