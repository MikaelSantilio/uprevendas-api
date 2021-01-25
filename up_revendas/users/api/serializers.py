from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.urls import reverse
from rest_framework import serializers

from up_revendas.users.models import Customer, Employee, Function, Profile

User = get_user_model()


class FunctionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Function
        fields = ["id", "name", "description", "salary"]


class UserIdSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "username"]


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('cpf', 'birth_date', 'phone_number')


class MyProfileSerializer(serializers.ModelSerializer):
    profile_detail = ProfileSerializer(source='profile')
    others = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["username", "email", "name", "profile_detail", "others"]

    def get_others(self, obj):
        data = {}

        request = self.context['request']

        if request.user.is_customer:
            data['customer-profile'] = request.build_absolute_uri(
                reverse("api:users:customer-profile"))

        if request.user.is_employee:
            data['employee-profile'] = request.build_absolute_uri(
                reverse("api:users:employee-profile"))

        if request.user.is_store_manager:
            data['store-manager'] = True

        return data


class UserHyperlinkSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    options = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('username', 'email', 'profile', 'options')

    def get_options(self, obj):
        data = {}

        request = self.context['request']

        if request.user.is_employee or request.user.is_store_manager or request.user.is_superuser:
            data['activate-customer'] = request.build_absolute_uri(
                reverse("api:users:activate-customer", kwargs={'pk': obj.id}))

        if request.user.is_store_manager or request.user.is_superuser:
            data['activate-employee'] = request.build_absolute_uri(
                reverse("api:users:activate-employee", kwargs={'pk': obj.id}))

        if request.user.is_superuser:
            data['activate-store-manager'] = request.build_absolute_uri(
                reverse("api:users:activate-store-manager", kwargs={'pk': obj.id}))

        return data


class CustomerSerializer(serializers.ModelSerializer):

    balance = serializers.FloatField(required=True)
    name = serializers.CharField(source='user.first_name')

    class Meta:
        model = Customer
        fields = ('user', 'name', 'balance')


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
    profile_detail = ProfileSerializer(source='profile')

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
            "profile_detail"
        ]


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["cpf", "birth_date", "phone_number"]


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["user", "function", "entry_date", "departure_date"]
