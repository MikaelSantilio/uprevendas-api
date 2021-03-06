# Generated by Django 3.0.11 on 2021-01-22 10:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cars', '0001_initial'),
        ('users', '0002_auto_20210122_0713'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank', models.CharField(max_length=32)),
                ('agency', models.CharField(max_length=16)),
                ('balance', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('value', models.FloatField()),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cars.Car')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.Customer')),
                ('seller', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('value', models.FloatField()),
                ('buyer_for', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cars.Car')),
                ('provider', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.Customer')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
