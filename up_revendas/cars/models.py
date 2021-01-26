from datetime import date

from django.core.validators import MinValueValidator
from django.db import models
from django.forms import ValidationError
from django.utils.translation import ugettext_lazy as _

from up_revendas.cars.validators import validateCarLicensePlate
from up_revendas.users.models import Base


class Brand(models.Model):
    name = models.CharField("Nome", max_length=32)

    def __str__(self):
        return self.name


class Model(models.Model):
    name = models.CharField("Nome", max_length=32)
    brand = models.ForeignKey(
        Brand, verbose_name="Marca", related_name="models", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.brand} {self.name}"


class Car(Base):

    YEAR_CHOICES = [
        (year, year) for year in range(1951, date.today().year + 1)
    ]

    # YEAR_CHOICES = (
    #     (2010, 2010),
    #     (2011, 2011),
    #     (2012, 2012),
    #     (2013, 2013),
    #     (2014, 2014),
    #     (2015, 2015),
    #     (2016, 2016),
    #     (2017, 2017),
    #     (2018, 2018),
    #     (2019, 2019),
    #     (2020, 2020),
    #     (2021, 2021)
    # )

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

    license_plate = models.CharField("Placa", max_length=8, validators=[validateCarLicensePlate])
    brand = models.ForeignKey(Brand, verbose_name="Marca", related_name="cars", on_delete=models.CASCADE)
    model = models.ForeignKey(Model, verbose_name="Modelo", related_name="cars", on_delete=models.CASCADE)
    year = models.IntegerField("Ano", choices=YEAR_CHOICES)
    version = models.CharField("Versão", max_length=255)
    transmission = models.CharField("Transmissão", max_length=14, choices=TRANSMISSION_CHOICES)
    mileage = models.IntegerField("Quilometragem", validators=[MinValueValidator(0)])
    car_type = models.CharField("Tipo do carro", max_length=12, choices=CAR_TYPES_CHOICES)
    color = models.CharField("Cor", max_length=12, choices=COLOR_CHOICES)
    min_sale_value = models.FloatField("Valor min. de venda", validators=[MinValueValidator(0)])
    sold = models.BooleanField("Vendido", default=False)

    def clean(self):
        if self.brand and self.model and self.brand != self.model.brand:
            raise ValidationError(message='O modelo não condiz com a marca', code='invalid')

    def __str__(self):
        return f"{self.brand.name} {self.model.name} {self.year} - {self.license_plate}"
