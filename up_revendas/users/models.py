from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from up_revendas.users.validators import validate_CPF, validate_phone


class User(AbstractUser):
    """Default user for UP Revendas."""

    #: First and last name do not cover name patterns around the globe
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    is_employee = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    is_store_manager = models.BooleanField(default=False)

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})


class Base(models.Model):
    created_at = models.DateTimeField('Created at', auto_now_add=True)
    updated_at = models.DateTimeField('Updated', auto_now=True)
    active = models.BooleanField('Active', default=True)

    class Meta:
        abstract = True


class Function(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField()
    salary = models.FloatField(validators=[MinValueValidator(0)])


class Profile(Base):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE, primary_key=True)
    cpf = models.CharField("CPF", unique=True, max_length=14, validators=[validate_CPF])
    birth_date = models.DateField()
    phone_number = models.CharField(validators=[validate_phone], max_length=17, blank=True)


class Employee(Base):
    user = models.OneToOneField(User, related_name='employee', on_delete=models.CASCADE, primary_key=True)
    function = models.ForeignKey(Function, on_delete=models.CASCADE)
    entry_date = models.DateField(auto_now_add=True)
    departure_date = models.DateField(null=True, blank=True)


class Customer(Base):
    user = models.OneToOneField(User, related_name='customer', on_delete=models.CASCADE, primary_key=True)
    balance = models.FloatField(validators=[MinValueValidator(0)])
