# Generated by Django 3.0.11 on 2021-01-26 23:52

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import up_revendas.cars.validators


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0007_auto_20210126_1543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='name',
            field=models.CharField(max_length=32, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='car',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Ativo'),
        ),
        migrations.AlterField(
            model_name='car',
            name='brand',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cars', to='cars.Brand', verbose_name='Marca'),
        ),
        migrations.AlterField(
            model_name='car',
            name='car_type',
            field=models.CharField(choices=[('hatch', 'Hatch'), ('sedan', 'Sedã'), ('suv', 'SUV'), ('van', 'Van/Utilitário'), ('pick-up', 'Pick-Up'), ('convertible', 'Conversível'), ('sport', 'Sport'), ('luxury', 'Luxo')], max_length=12, verbose_name='Tipo do carro'),
        ),
        migrations.AlterField(
            model_name='car',
            name='color',
            field=models.CharField(choices=[('black', 'Preto'), ('white', 'Branco'), ('silver', 'Prata'), ('red', 'Vermelho'), ('cinza', 'Cinza'), ('blue', 'Azul'), ('yellow', 'Amarelo'), ('green', 'Verde'), ('orange', 'Laranja'), ('other', 'Outra')], max_length=12, verbose_name='Cor'),
        ),
        migrations.AlterField(
            model_name='car',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Criado em'),
        ),
        migrations.AlterField(
            model_name='car',
            name='license_plate',
            field=models.CharField(max_length=8, validators=[up_revendas.cars.validators.validateCarLicensePlate], verbose_name='Placa'),
        ),
        migrations.AlterField(
            model_name='car',
            name='mileage',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Quilometragem'),
        ),
        migrations.AlterField(
            model_name='car',
            name='min_sale_value',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Valor min. de venda'),
        ),
        migrations.AlterField(
            model_name='car',
            name='model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cars', to='cars.Model', verbose_name='Modelo'),
        ),
        migrations.AlterField(
            model_name='car',
            name='sold',
            field=models.BooleanField(default=False, verbose_name='Vendido'),
        ),
        migrations.AlterField(
            model_name='car',
            name='transmission',
            field=models.CharField(choices=[('M', 'Manual'), ('AT', 'Automatic'), ('SA', 'Semi Automatic')], max_length=14, verbose_name='Transmissão'),
        ),
        migrations.AlterField(
            model_name='car',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Atualizado em'),
        ),
        migrations.AlterField(
            model_name='car',
            name='version',
            field=models.CharField(max_length=255, verbose_name='Versão'),
        ),
        migrations.AlterField(
            model_name='car',
            name='year',
            field=models.IntegerField(choices=[(1951, 1951), (1952, 1952), (1953, 1953), (1954, 1954), (1955, 1955), (1956, 1956), (1957, 1957), (1958, 1958), (1959, 1959), (1960, 1960), (1961, 1961), (1962, 1962), (1963, 1963), (1964, 1964), (1965, 1965), (1966, 1966), (1967, 1967), (1968, 1968), (1969, 1969), (1970, 1970), (1971, 1971), (1972, 1972), (1973, 1973), (1974, 1974), (1975, 1975), (1976, 1976), (1977, 1977), (1978, 1978), (1979, 1979), (1980, 1980), (1981, 1981), (1982, 1982), (1983, 1983), (1984, 1984), (1985, 1985), (1986, 1986), (1987, 1987), (1988, 1988), (1989, 1989), (1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021)], verbose_name='Ano'),
        ),
        migrations.AlterField(
            model_name='model',
            name='brand',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='models', to='cars.Brand', verbose_name='Marca'),
        ),
        migrations.AlterField(
            model_name='model',
            name='name',
            field=models.CharField(max_length=32, verbose_name='Nome'),
        ),
    ]