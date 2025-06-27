from django_filters import rest_framework as filters
from django.contrib.auth import get_user_model

User = get_user_model()

class UserFilter(filters.FilterSet):
    is_manager = filters.BooleanFilter(method='filter_is_manager')
    is_mechanic = filters.BooleanFilter(method='filter_is_mechanic')

    class Meta:
        model = User
        fields = ['is_superuser', 'is_manager', 'is_mechanic']

    def filter_is_manager(self, queryset, name, value):
        if value:
            return queryset.filter(manager__isnull=False)
        return queryset.filter(manager__isnull=True)

    def filter_is_mechanic(self, queryset, name, value):
        if value:
            return queryset.filter(mechanic__isnull=False)
        return queryset.filter(mechanic__isnull=True)