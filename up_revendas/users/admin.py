from django.contrib import admin
from django.contrib.auth import get_user_model

from up_revendas.users.models import Customer, Employee, Function, Profile

User = get_user_model()


admin.site.register(User)
admin.site.register(Function)
admin.site.register(Profile)
admin.site.register(Customer)
admin.site.register(Employee)
