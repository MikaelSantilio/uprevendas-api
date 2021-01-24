# Generated by Django 3.0.11 on 2021-01-24 19:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20210123_1431'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='bank_account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.BankAccount'),
        ),
        migrations.AddField(
            model_name='sale',
            name='bank_account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.BankAccount'),
        ),
    ]
