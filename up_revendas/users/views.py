from django.contrib.auth import get_user_model
from django.db import transaction
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.generics import (
    GenericAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from up_revendas.core.permissions import IsEmployee, IsStoreManager
from up_revendas.core.views import ListPaginatedMixin
from up_revendas.users.filters import UserFilter
from up_revendas.users.models import Function
from up_revendas.users.serializers import (
    CreateUserSerializer,
    CustomerSerializer,
    EmployeeSerializer,
    FunctionSerializer,
    MyProfileSerializer,
    ProfileDetailSerializer,
    UserHATEOASerializer,
    UserListSerializer,
)

User = get_user_model()


class FunctionListCreateAPIView(ListCreateAPIView):
    queryset = Function.objects.all()
    serializer_class = FunctionSerializer
    permission_classes = [IsAdminUser | IsStoreManager]


class FunctionRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Function.objects.all()
    serializer_class = FunctionSerializer
    permission_classes = [IsAdminUser | IsStoreManager]


class CreateUserAPIView(APIView):

    permission_classes = [IsAdminUser | IsStoreManager | IsEmployee]

    def post(self, request, format=None):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            data = UserHATEOASerializer(user, context={'request': request}).data
            # pdb.set_trace()

            return Response(status=status.HTTP_200_OK, data=data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)


class ActivateStoreManagerAPIView(APIView):

    permission_classes = [IsAdminUser]

    def post(self, request, pk=None, format=None):
        user = get_object_or_404(User, pk=pk)
        if user.is_store_manager:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'detail': 'Administrador já ativado'})
        user.is_store_manager = True
        user.save()
        return Response(status=status.HTTP_200_OK, data={'detail': 'Administrador da loja ativado com sucesso'})


class ActivateCustomerAPIView(APIView):

    permission_classes = [IsAdminUser | IsStoreManager | IsEmployee]

    def post(self, request, pk=None, format=None):
        user = get_object_or_404(User, pk=pk)

        if user.is_customer and user.customer:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'detail': 'Cliente já ativado'})

        customer_data = request.data
        customer_data['user'] = pk

        serializer = CustomerSerializer(data=customer_data, context={"request": request})
        if serializer.is_valid():
            self.save_data(serializer, user)
            return Response(status=status.HTTP_200_OK, data={'detail': 'Cliente ativado com sucesso'})

        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    @transaction.atomic
    def save_data(self, serializer, user):
        user.is_customer = True
        serializer.save()
        user.save()


class ActivateEmployeeAPIView(APIView):

    permission_classes = [IsAdminUser | IsStoreManager]

    def post(self, request, pk=None, format=None):
        user = get_object_or_404(User, pk=pk)

        if user.is_employee and user.employee:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'detail': 'Funcionário já ativado'})

        employee_data = request.data
        employee_data['user'] = pk

        serializer = EmployeeSerializer(data=employee_data, context={"request": request})
        if serializer.is_valid():
            self.save_data(serializer, user)

            return Response(status=status.HTTP_200_OK, data={'detail': 'Funcionário ativado com sucesso'})

        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    @transaction.atomic
    def save_data(self, serializer, user):
        user.is_employee = True
        serializer.save()
        user.save()


class MyProfileAPIView(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request, format=None):
        serializer = MyProfileSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class ProfileDetailAPIView(APIView):

    permission_classes = [IsAdminUser | IsStoreManager | IsEmployee]

    def get(self, request, pk, format=None):
        user = get_object_or_404(User, pk=pk)
        serializer = ProfileDetailSerializer(user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class UserListAPIView(ListPaginatedMixin, GenericAPIView):

    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAdminUser | IsStoreManager | IsEmployee]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = UserFilter
    # filterset_fields = ['is_employee', 'is_customer', 'is_store_manager']
    ordering_fields = ['username']

    def get(self, request, format=None):
        return self.custom_paginated_queryset(request, UserListSerializer)

        # serializer = UserListSerializer(users, many=True, context={"request": request})
        # return Response(status=status.HTTP_200_OK, data=serializer.data)
