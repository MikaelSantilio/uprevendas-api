from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

from up_revendas.users.forms import UserChangeForm, UserCreationForm
from up_revendas.users.models import Customer, Employee, Function, Profile

User = get_user_model()


# @admin.register(User)
# class UserAdmin(auth_admin.UserAdmin):

#     form = UserChangeForm
#     add_form = UserCreationForm
#     fieldsets = (("User", {"fields": ("name",)}),) + tuple(
#         auth_admin.UserAdmin.fieldsets
#     )
#     list_display = ["username", "name", "is_superuser"]
#     search_fields = ["name"]


admin.site.register(User)
admin.site.register(Function)
admin.site.register(Profile)
admin.site.register(Customer)
admin.site.register(Employee)
