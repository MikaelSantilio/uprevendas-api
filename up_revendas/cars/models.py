from datetime import date

from django.core.validators import MinValueValidator
from django.db import models
from django.forms import ValidationError
from django.utils.translation import ugettext_lazy as _

from up_revendas.cars.validators import validateCarLicensePlate
from up_revendas.users.models import Base


class Brand(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Model(models.Model):
    name = models.CharField(max_length=32)
    brand = models.ForeignKey(Brand,  related_name="models", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.brand} {self.name}"


class Car(Base):

    YEAR_CHOICES = [
        (year, year) for year in range(1951, date.today().year + 1)
    ]

    CAR_TYPES_CHOICES = (
        ("hatch", "Hatch"),
        ("sedan", "Sedã"),
        ("suv", "SUV"),
        ("van", "Van/Utilitário"),
        ("pick-up", "Pick-Up"),
        ("convertible", "Conversível"),
        ("sport", "Sport"),
        ("luxury", "Luxo"),
    )

    COLOR_CHOICES = (
        ("black", "Preto"),
        ("white", "Branco"),
        ("silver", "Prata"),
        ("red", "Vermelho"),
        ("cinza", "Cinza"),
        ("blue", "Azul"),
        ("yellow", "Amarelo"),
        ("green", "Verde"),
        ("orange", "Laranja"),
        ("other", "Outra"),
    )

    TRANSMISSION_CHOICES = (
        ("M", _("Manual")),
        ("AT", _("Automatic")),
        ("SA", _("Semi Automatic"))
    )

    license_plate = models.CharField(max_length=8, validators=[validateCarLicensePlate])
    brand = models.ForeignKey(Brand, related_name="cars", on_delete=models.CASCADE)
    model = models.ForeignKey(Model, related_name="cars", on_delete=models.CASCADE)
    year = models.CharField(max_length=4, choices=YEAR_CHOICES)
    version = models.CharField(max_length=255)
    transmission = models.CharField(max_length=14, choices=TRANSMISSION_CHOICES)
    mileage = models.IntegerField(validators=[MinValueValidator(0)])
    car_type = models.CharField(max_length=12, choices=CAR_TYPES_CHOICES)
    color = models.CharField(max_length=12, choices=COLOR_CHOICES)
    min_sale_value = models.FloatField(validators=[MinValueValidator(0)])
    sold = models.BooleanField(default=False)

    def clean(self):
        if self.brand and self.model and self.brand != self.model.brand:
            raise ValidationError(message='O modelo não condiz com a marca', code='invalid')
