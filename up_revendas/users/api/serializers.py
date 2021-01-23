from django.contrib.auth import get_user_model
from rest_framework import serializers
from up_revendas.users.models import Employee, Customer, Profile

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        ref_name = "User 1"
        fields = ["username", "email", "name", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        }


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        ref_name = "User 1"
        fields = [
            "id",
            "username",
            "email",
            "name",
            "is_employee",
            "is_customer",
            "is_store_manager",
            # "profile-url",
            "customer_url",
            "employee_url"
        ]

        extra_kwargs = {
            # "profile-url": {"view_name": "api:user-detail", "lookup_field": "username"},
            "customer_url": {"view_name": "api:customer-profile", "lookup_field": "id"},
            "employee_url": {"view_name": "api:employee-profile", "lookup_field": "id"},
        }


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["cpf", "birth_date", "phone_number"]


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["balance"]


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["function", "entry_date"]
