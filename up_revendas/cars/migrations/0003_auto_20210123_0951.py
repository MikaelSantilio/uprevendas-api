# Generated by Django 3.0.11 on 2021-01-23 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0002_auto_20210123_0921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='transmission',
            field=models.CharField(choices=[('M', 'Manual'), ('AT', 'Automatic'), ('SA', 'Semi Automatic')], max_length=14),
        ),
        migrations.AlterField(
            model_name='car',
            name='version',
            field=models.CharField(max_length=255),
        ),
        migrations.DeleteModel(
            name='Version',
        ),
    ]
