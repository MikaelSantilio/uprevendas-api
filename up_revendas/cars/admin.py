from django.contrib import admin

from up_revendas.cars.models import Brand, Car, Model

admin.site.register(Brand)
admin.site.register(Model)
admin.site.register(Car)
