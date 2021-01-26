from django.core.validators import MinValueValidator
from django.db import models

from up_revendas.cars.models import Car
from up_revendas.users.models import Base, Customer, User
from up_revendas.users.validators import validate_CPF


class BankAccount(models.Model):
    bank = models.CharField("Banco", max_length=32)
    agency = models.CharField("Agência", max_length=16)
    account_type = models.CharField("Tipo de conta", max_length=32)
    name = models.CharField("Nome", max_length=32)
    cpf = models.CharField("CPF", max_length=14, validators=[validate_CPF])
    balance = models.FloatField("Saldo", validators=[MinValueValidator(0)])


class Purchase(Base):
    provider = models.ForeignKey(
        Customer, verbose_name="Fornecedor", related_name="purchases", null=True, on_delete=models.SET_NULL)
    buyer_for = models.ForeignKey(
        User, verbose_name="Comprador por", related_name="purchases", null=True, on_delete=models.SET_NULL)
    car = models.ForeignKey(Car, verbose_name="Carro", related_name="purchases", on_delete=models.CASCADE)
    value = models.FloatField("valor", validators=[MinValueValidator(0)])
    bank_account = models.ForeignKey(
        BankAccount,
        verbose_name="Conta bancária", related_name="purchases", null=True, blank=True, on_delete=models.SET_NULL)


class Sale(Base):
    customer = models.ForeignKey(
        Customer, verbose_name="Cliente", related_name="sales", null=True, blank=True, on_delete=models.SET_NULL)
    seller = models.ForeignKey(
        User, verbose_name="Vendido por", related_name="sales", null=True, on_delete=models.SET_NULL)
    car = models.ForeignKey(Car, verbose_name="Carro", related_name="sales", on_delete=models.CASCADE)
    value = models.FloatField(validators=[MinValueValidator(0)])
    bank_account = models.ForeignKey(
        BankAccount,
        verbose_name="Conta bancária", related_name="sales", null=True, blank=True, on_delete=models.SET_NULL)
