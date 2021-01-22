from django.db import models
from datetime import date
from up_revendas.cars.validators import validateCarLicensePlate
from up_revendas.core.models import Base
from django.utils.translation import ugettext_lazy as _


class Brand(Base):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Model(Base):
    name = models.CharField(max_length=32)
    brand = models.ForeignKey(Brand,  related_name="models", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.brand} {self.name}"


class Version(Base):
    name = models.CharField(max_length=32)
    model = models.ForeignKey(Model, related_name="versions", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.model.brand} {self.name}"


class Car(Base):

    YEAR_CHOICES = (
        (year, year) for year in range(1951, date.today().year + 1)
    )

    TRANSMISSION_CHOICES = (
        ("M", _("Manual")),
        ("A", _("Automatic")),
        ("SA", _("Semi Automatic"))
    )

    license_plate = models.CharField(max_length=8, validators=[validateCarLicensePlate])
    brand = models.ForeignKey(Brand, related_name="cars", on_delete=models.CASCADE)
    model = models.ForeignKey(Model, related_name="cars", on_delete=models.CASCADE)
    year = models.CharField(max_length=4, choices=YEAR_CHOICES)
    version = models.ForeignKey(Version, related_name="cars", on_delete=models.CASCADE)
    # transmission = models.CharField(max_length=14, choices=TRANSMISSION_CHOICES)
    # https://en.wikipedia.org/wiki/Power_steering
    sale_value = models.FloatField()
    sold = models.BooleanField(default=False)
