from rest_framework import serializers
from .models import Call
from incidents.models import Incident

class CallSerializer(serializers.ModelSerializer):
    incident = serializers.SlugRelatedField(
        queryset=Incident.objects.all(),
        slug_field="incident_id",
        required=False,  # if you want it optional
        allow_null=True
    )

    class Meta:
        model = Call
        fields = [
            "id",
            "call_sid",
            "caller_number",
            "incident",
            "timestamp",
            "completed_at",
            "duration_seconds"
        ]
        read_only_fields = ["id", "timestamp", "completed_at", "duration_seconds"]
