from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response


from up_revendas.cars.models import Brand, Car, Model
from up_revendas.cars.serializers import (
    BrandSerializer,
    CarHyperlinkSerializer,
    CarSerializer,
    ModelSerializer
)


class BrandListCreateAPIView(ListCreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['name']


class BrandRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [AllowAny]


class ModelListCreateAPIView(ListCreateAPIView):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['brand', 'name']
    ordering_fields = ['name']


class ModelRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer
    permission_classes = [AllowAny]


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


class CarChoicesAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, format=None):

        data = {
            'transmissions': Car.TRANSMISSION_CHOICES,
            'car_types': Car.CAR_TYPES_CHOICES,
            'colors': Car.COLOR_CHOICES,
            'years': Car.YEAR_CHOICES
        }

        return Response(data, status=status.HTTP_200_OK)
