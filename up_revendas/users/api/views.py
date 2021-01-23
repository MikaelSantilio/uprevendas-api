from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import AllowAny, IsAdminUser

from up_revendas.users.api.serializers import (
    CustomerSerializer,
    EmployeeSerializer,
    UserSerializer,
)

User = get_user_model()


class UserViewSet(GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "id"

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(id=self.request.user.id)

    def get_permissions(self):
        if self.action == 'profile':
            return [IsAdminUser(), ]        
        return super(UserViewSet, self).get_permissions()

    def create_store_manager(self):
        pass

    def create_customer(self):
        pass

    def create_employee(self):
        pass

    @action(detail=False, methods=["GET"])
    def profile(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(detail=False, methods=["GET"])
    def customer_profile(self, request, url_path="customer-profile"):
        if request.user.is_customer and request.user.customer:
            serializer = CustomerSerializer(request.user.customer, context={"request": request})
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=["GET"], url_path="employee-profile")
    def employee_profile(self, request):
        if request.user.is_employee and request.user.employee:
            serializer = EmployeeSerializer(request.user.employee, context={"request": request})
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)
