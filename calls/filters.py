import django_filters
from .models import Call

class CallFilter(django_filters.FilterSet):
    caller_number = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Call
        fields = ["caller_number"]
