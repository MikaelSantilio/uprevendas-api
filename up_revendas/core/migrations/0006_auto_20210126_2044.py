# Generated by Django 3.0.11 on 2021-01-26 23:44

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0005_auto_20210123_1848'),
        ('cars', '0007_auto_20210126_1543'),
        ('core', '0005_auto_20210125_1724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankaccount',
            name='account_type',
            field=models.CharField(max_length=32, verbose_name='Tipo de conta'),
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='agency',
            field=models.CharField(max_length=16, verbose_name='Agência'),
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='balance',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Saldo'),
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='bank',
            field=models.CharField(max_length=32, verbose_name='Banco'),
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='name',
            field=models.CharField(max_length=32, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='bank_account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='purchases', to='core.BankAccount', verbose_name='Conta bancária'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='buyer_for',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='purchases', to=settings.AUTH_USER_MODEL, verbose_name='Comprador por'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='car',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchases', to='cars.Car', verbose_name='Carro'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='provider',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='purchases', to='users.Customer', verbose_name='Fornecedor'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='value',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='valor'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='bank_account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sales', to='core.BankAccount', verbose_name='Conta bancária'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='car',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales', to='cars.Car', verbose_name='Carro'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sales', to='users.Customer', verbose_name='Cliente'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='seller',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sales', to=settings.AUTH_USER_MODEL, verbose_name='Vendido por'),
        ),
    ]