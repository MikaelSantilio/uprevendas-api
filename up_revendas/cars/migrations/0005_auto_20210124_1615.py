# Generated by Django 3.0.11 on 2021-01-24 19:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0004_auto_20210123_1431'),
    ]

    operations = [
        migrations.RenameField(
            model_name='car',
            old_name='sale_value',
            new_name='min_sale_value',
        ),
    ]
