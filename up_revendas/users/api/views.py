import pdb

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from up_revendas.users.api.serializers import (
    CreateUserSerializer,
    CustomerSerializer,
    EmployeeSerializer,
    UserHyperlinkSerializer,
    UserSerializer,
)

User = get_user_model()


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

        user.is_customer = True

        customer_data = request.data
        customer_data['user'] = pk

        serializer = CustomerSerializer(data=customer_data, context={"request": request})
        if serializer.is_valid():
            return Response(status=status.HTTP_200_OK, data={'detail': 'Cliente ativado com sucesso'})

        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)


class ActivateEmployeeAPIView(APIView):

    permission_classes = (AllowAny, )

    def put(self, request, pk=None, format=None):
        user = get_object_or_404(User, pk=pk)

        if user.is_employee and user.employee:
            return Response(status=status.HTTP_204_NO_CONTENT, data={'detail': 'Funcionário já ativado'})

        user.is_employee = True

        employee_data = request.data
        employee_data['user'] = pk

        serializer = EmployeeSerializer(data=employee_data, context={"request": request})
        if serializer.is_valid():
            return Response(status=status.HTTP_200_OK, data={'detail': 'Funcionário ativado com sucesso'})

        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)


class ProfileDetailAPIView(APIView):

    permission_classes = (AllowAny, )

    def get(self, request, format=None):
        serializer = UserSerializer(request.user, context={"request": request})
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
