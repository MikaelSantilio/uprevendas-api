from django.db import models

from up_revendas.cars.models import Car
from up_revendas.users.models import Customer, User


class Base(models.Model):
    created_at = models.DateTimeField('Created at', auto_now_add=True)
    updated_at = models.DateTimeField('Updated', auto_now=True)
    active = models.BooleanField('Active', default=True)

    class Meta:
        abstract = True


class BankAccount(models.Model):
    bank = models.CharField(max_length=32)
    agency = models.CharField(max_length=16)
    balance = models.FloatField(default=0)


class Purchase(Base):
    provider = models.ForeignKey(Customer, on_delete=models.SET_NULL)
    responsible = models.ForeignKey(User, on_delete=models.SET_NULL)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    value = models.FloatField()


class Sale(Base):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL)
    responsible = models.ForeignKey(User, on_delete=models.SET_NULL)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    value = models.FloatField()
