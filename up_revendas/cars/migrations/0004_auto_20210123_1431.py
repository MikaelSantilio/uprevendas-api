# Generated by Django 3.0.11 on 2021-01-23 17:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0003_auto_20210123_0951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='mileage',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='car',
            name='sale_value',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
