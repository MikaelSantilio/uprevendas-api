from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from up_revendas.cars.models import Brand, Car, Model
from up_revendas.cars.serializers import (
    BrandSerializer,
    CarDetailSerializer,
    CarHyperlinkSerializer,
    CarSerializer,
    ModelSerializer,
)
from up_revendas.core.permissions import IsEmployee, IsStoreManager


class BrandListCreateAPIView(ListCreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['name']

    def check_create_permissions(self, request):

        permission = [IsAdminUser | IsStoreManager | IsEmployee][0]()
        if not permission.has_permission(request, self):
            self.permission_denied(
                request,
                message=getattr(permission, 'message', None),
                code=getattr(permission, 'code', None)
            )

    def post(self, request, *args, **kwargs):
        self.check_create_permissions(request)
        return self.create(request, *args, **kwargs)


class BrandRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAdminUser | IsStoreManager | IsEmployee]


class ModelListCreateAPIView(ListCreateAPIView):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['brand', 'name']
    ordering_fields = ['name']

    def check_create_permissions(self, request):

        permission = [IsAdminUser | IsStoreManager | IsEmployee][0]()
        if not permission.has_permission(request, self):
            self.permission_denied(
                request,
                message=getattr(permission, 'message', None),
                code=getattr(permission, 'code', None)
            )

    def post(self, request, *args, **kwargs):
        self.check_create_permissions(request)
        return self.create(request, *args, **kwargs)


class ModelRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer
    permission_classes = [IsAdminUser | IsStoreManager | IsEmployee]


class CarHyperlinkListCreateAPIView(ListCreateAPIView):
    queryset = Car.objects.filter(sold=False)
    serializer_class = CarSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['brand', 'model', 'car_type', 'color', 'transmission']
    ordering_fields = ['sale_value', 'mileage', 'year', 'version']
    # ordering = ['sale_value']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = CarHyperlinkSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = CarHyperlinkSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)


class CarRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsAdminUser | IsStoreManager]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = CarDetailSerializer(instance)
        return Response(serializer.data)


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
