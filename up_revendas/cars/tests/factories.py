from factory import (
    Faker,
    DjangoModelFactory,
    SubFactory,
)
from account.tests.factories import ProfileFactory

from account.tests.factories import UserFactory
from up_revendas.cars.models import Car


class CarFactory(DjangoModelFactory):

    class Meta:
        model = Car

    license_plate = models.CharField(max_length=8, validators=[validateCarLicensePlate])
    brand = models.ForeignKey(Brand, related_name="cars", on_delete=models.CASCADE)
    model = models.ForeignKey(Model, related_name="cars", on_delete=models.CASCADE)
    year = models.CharField(max_length=4, choices=YEAR_CHOICES)
    version = models.ForeignKey(Version, related_name="cars", on_delete=models.CASCADE)
    transmission = models.CharField(max_length=14, choices=TRANSMISSION_CHOICES)
    mileage = models.IntegerField(min)
    car_type = models.CharField(max_length=12, choices=CAR_TYPES_CHOICES)
    color = models.CharField(max_length=12, choices=COLOR_CHOICES)
    sale_value = models.FloatField()
    sold = models.BooleanField(default=False)
