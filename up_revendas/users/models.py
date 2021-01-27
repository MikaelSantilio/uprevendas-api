from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models

from up_revendas.users.validators import validate_CPF, validate_phone


class User(AbstractUser):
    """Default user for UP Revendas."""

    name = models.CharField("Nome", blank=True, max_length=255)
    is_employee = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    is_store_manager = models.BooleanField(default=False)


class Base(models.Model):
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    active = models.BooleanField('Ativo', default=True)

    class Meta:
        abstract = True


class Function(models.Model):
    name = models.CharField("Nome", max_length=32)
    description = models.TextField("Descrição")
    salary = models.FloatField("Salário", validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.name} - R$ {self.salary:.2f}"


class Profile(Base):
    user = models.OneToOneField(
        User, verbose_name="Usuário", related_name='profile', on_delete=models.CASCADE, primary_key=True)
    cpf = models.CharField("CPF", unique=True, max_length=14, validators=[validate_CPF])
    birth_date = models.DateField("Data. nasc.")
    phone_number = models.CharField("Telefone", validators=[validate_phone], max_length=17, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.cpf}"


class Employee(Base):
    user = models.OneToOneField(
        User, verbose_name="Usuário", related_name='employee', on_delete=models.CASCADE, primary_key=True)
    function = models.ForeignKey(Function, verbose_name="Função", related_name="employees", on_delete=models.CASCADE)
    entry_date = models.DateField("Data de entrada", auto_now_add=True)
    departure_date = models.DateField("Data de saída", null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.function.name}"


class Customer(Base):
    user = models.OneToOneField(
        User, verbose_name="Usuário", related_name='customer', on_delete=models.CASCADE, primary_key=True)
    balance = models.FloatField("Saldo", validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.user.username} - R$ {self.balance:.2f}"
