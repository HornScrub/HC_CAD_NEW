import django_filters
from .models import Call

class CallFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=Call.STATUS_CHOICES)
    priority_level = django_filters.ChoiceFilter(choices=Call.STATUS_CHOICES)

    class Meta:
        model = Call
        fields = ["status", "caller_number", "priority_level"]
