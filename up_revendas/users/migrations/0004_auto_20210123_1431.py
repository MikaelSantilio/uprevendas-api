# Generated by Django 3.0.11 on 2021-01-23 17:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_is_store_manager'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='balance',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='function',
            name='salary',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
