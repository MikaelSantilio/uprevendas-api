from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.urls import reverse
from rest_framework import serializers

from up_revendas.users.models import Customer, Employee, Profile

User = get_user_model()


class UserIdSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "username"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        ref_name = "User 1"
        fields = ["username", "email", "name", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        }


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('cpf', 'birth_date', 'phone_number')


class UserHyperlinkSerializer(serializers.ModelSerializer):
    # profile = ProfileSerializer()
    options = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('username', 'email', 'options')

    def get_options(self, obj):
        data = {}

        # data = {
        #     'activate-customer': reverse("api:users:activate-customer", kwargs={'pk': obj.id}),
        #     'activate-employee': reverse("api:users:activate-employee", kwargs={'pk': obj.id}),
        #     'activate-store-manager': reverse("api:users:activate-store-manager", kwargs={'pk': obj.id}),
        # }
        if self.context['request'].is_employee:
            data['activate-customer'] = reverse("api:users:activate-customer", kwargs={'pk': obj.id})

        if self.context['request'].is_store_manager:
            data['activate-employee'] = reverse("api:users:activate-employee", kwargs={'pk': obj.id})

        if self.context['request'].is_superuser:
            data['activate-store-manager'] = reverse("api:users:activate-store-manager", kwargs={'pk': obj.id}),

        return data


class CustomerSerializer(serializers.ModelSerializer):

    balance = serializers.FloatField(required=True)

    class Meta:
        model = Customer
        fields = ('id', 'user', 'balance')


class CreateUserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'profile', 'password')

    @transaction.atomic
    def create(self, validated_data):

        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            password=make_password(validated_data['password'])
        )

        profile_data = validated_data.pop('profile')

        profile = Profile.objects.create(
            user=user,
            cpf=profile_data['cpf'],
            birth_date=profile_data['birth_date'],
            phone_number=profile_data['phone_number']
        )

        return user


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


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["function", "entry_date"]
