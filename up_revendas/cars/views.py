from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action


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


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.filter(sold=False)
    serializer_class = CarSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['brand', 'model', 'car_type', 'color', 'transmission']
    ordering_fields = ['sale_value', 'mileage', 'year', 'version']

    def get_permissions(self):

        if self.action == 'list':
            permission_classes = [AllowAny]
        elif self.action == 'choices':
            permission_classes = [AllowAny]
        elif self.action == 'retrieve':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser | IsStoreManager]
        return [permission() for permission in permission_classes]

    def list(self, request):
        queryset = self.get_queryset()
        serializer = CarHyperlinkSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def choices(self, request, format=None):
        data = {
            'transmissions': Car.TRANSMISSION_CHOICES,
            'car_types': Car.CAR_TYPES_CHOICES,
            'colors': Car.COLOR_CHOICES,
            'years': Car.YEAR_CHOICES
        }

        return Response(data, status=status.HTTP_200_OK)

    # def create(self, request):
    #     serializer = CarSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def retrieve(self, request, pk=None):
    #     obj = get_object_or_404(Car, pk=pk)
    #     serializer = CarSerializer(obj)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    # def update(self, request, pk=None):
    #     pass

    # def partial_update(self, request, pk=None):
    #     pass

    # def destroy(self, request, pk=None):
    #     pass
