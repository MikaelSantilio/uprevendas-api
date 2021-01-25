from django.core.validators import MinValueValidator
from django.db import models

from up_revendas.cars.models import Car
from up_revendas.users.models import Base, Customer, User
from up_revendas.users.validators import validate_CPF


class BankAccount(models.Model):
    bank = models.CharField(max_length=32)
    agency = models.CharField(max_length=16)
    account_type = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    cpf = models.CharField("CPF", max_length=14, validators=[validate_CPF])
    balance = models.FloatField(validators=[MinValueValidator(0)])


class Purchase(Base):
    provider = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    buyer_for = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    value = models.FloatField(validators=[MinValueValidator(0)])
    bank_account = models.ForeignKey(BankAccount, null=True, blank=True, on_delete=models.SET_NULL)


class Sale(Base):
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
    seller = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    value = models.FloatField(validators=[MinValueValidator(0)])
    bank_account = models.ForeignKey(BankAccount, null=True, blank=True, on_delete=models.SET_NULL)
