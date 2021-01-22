from django.db import models

from up_revendas.cars.models import Car
from up_revendas.users.models import Base, Customer, User


class BankAccount(models.Model):
    bank = models.CharField(max_length=32)
    agency = models.CharField(max_length=16)
    balance = models.FloatField(default=0)


class Purchase(Base):
    provider = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    buyer_for = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    value = models.FloatField()


class Sale(Base):
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
    seller = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    value = models.FloatField()
