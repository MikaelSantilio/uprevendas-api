from django.contrib import admin
from up_revendas.core.models import BankAccount, Purchase, Sale

admin.site.register(BankAccount)
admin.site.register(Purchase)
admin.site.register(Sale)