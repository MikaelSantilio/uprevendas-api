import pdb

from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from up_revendas.core.permissions import IsStoreManager
from up_revendas.users.api.serializers import (
    CreateUserSerializer,
    CustomerSerializer,
    EmployeeSerializer,
    FunctionSerializer,
    MyProfileSerializer,
    ProfileSerializer,
    UserHyperlinkSerializer,
    UserIdSerializer,
    UserProfileSerializer,
)
from up_revendas.users.models import Customer, Function
from django.db import transaction

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

    permission_classes = (AllowAny, )

    def post(self, request, format=None):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            data = UserHyperlinkSerializer(user).data
            # pdb.set_trace()

            return Response(status=status.HTTP_200_OK, data=data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)


class ActivateStoreManagerAPIView(APIView):

    permission_classes = (AllowAny, )

    def put(self, request, pk=None, format=None):
        user = get_object_or_404(User, pk=pk)
        user.is_store_manager = True
        user.save()
        return Response(status=status.HTTP_200_OK, data={'detail': 'Administrador da loja ativado com sucesso'})


class ActivateCustomerAPIView(APIView):

    permission_classes = (AllowAny, )

    def put(self, request, pk=None, format=None):
        user = get_object_or_404(User, pk=pk)

        if user.is_customer and user.customer:
            return Response(status=status.HTTP_204_NO_CONTENT, data={'detail': 'Cliente já ativado'})

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

    permission_classes = (AllowAny, )

    def put(self, request, pk=None, format=None):
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

    permission_classes = (AllowAny, )

    def get(self, request, pk, format=None):
        user = get_object_or_404(User, pk=pk)
        serializer = UserProfileSerializer(user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class CustomerDetailAPIView(APIView):

    permission_classes = (AllowAny, )

    def get(self, request, format=None):
        if request.user.is_customer and request.user.customer:
            serializer = CustomerSerializer(request.user.customer, context={"request": request})
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)


class EmployeeDetailAPIView(APIView):

    permission_classes = (AllowAny, )

    def get(self, request, format=None):
        if request.user.is_employee and request.user.employee:
            serializer = EmployeeSerializer(request.user.employee, context={"request": request})
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)


class SellersListAPIView(APIView):

    permission_classes = (AllowAny, )

    def get(self, request, format=None):
        users = User.objects.filter(Q(is_employee=True) | Q(is_store_manager=True))
        serializer = UserIdSerializer(users, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class CustomersListAPIView(APIView):

    permission_classes = (AllowAny, )

    def get(self, request, format=None):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
