from django.contrib.auth import get_user_model
from django.db.models import Q
from django_filters import rest_framework as filters

User = get_user_model()


class UserFilter(filters.FilterSet):
    is_seller = filters.BooleanFilter(
        field_name='is_employee', lookup_expr='is_seller', method='get_sellers')

    def get_sellers(self, queryset, field_name, value):
        return queryset.filter(Q(is_employee=True) | Q(is_store_manager=True))

    class Meta:
        model = User
        fields = ['is_employee', 'is_customer', 'is_store_manager', 'is_seller']
