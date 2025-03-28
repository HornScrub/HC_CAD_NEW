from rest_framework import serializers
from units.models import Unit
from .models import Incident, TrafficStop
from records.models import Subject, Vehicle, Call

class IncidentSerializer(serializers.ModelSerializer):
    assigned_units = serializers.SlugRelatedField(
        queryset=Unit.objects.all(),
        slug_field="identifier",
        many=True
    )

    class Meta:
        model = Incident
        fields = [
            "incident_id",
            "title",
            "emergency_type",
            "location",
            "status",
            "priority_level",
            "assigned_units",
            "created_at",
            "resolved_at"
        ]
        read_only_fields = ["incident_id", "created_at", "resolved_at"]

class TrafficStopSerializer(serializers.ModelSerializer):
    officer = serializers.SlugRelatedField(
        queryset=Unit.objects.all(),
        slug_field="identifier",
        required=False,
        allow_null=True
    )
    subject = serializers.SlugRelatedField(
        queryset=Subject.objects.all(),
        slug_field="subject_uid",
        required=False,
        allow_null=True
    )
    vehicle = serializers.SlugRelatedField(
        queryset=Vehicle.objects.all(),
        slug_field="license_plate",
        required=False,
        allow_null=True
    )
    call = serializers.SlugRelatedField(
        queryset=Call.objects.all(),
        slug_field="call_sid",
        required=False,
        allow_null=True
    )
    reason = serializers.CharField(required=False, allow_blank=True)
    outcome = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = TrafficStop
        fields = [
            "incident_id",
            "title",
            "emergency_type",
            "location",
            "status",
            "priority_level",
            "officer",
            "subject",
            "vehicle",
            "call",
            "reason",
            "outcome",
            "citation_issued",
            "timestamp"
        ]
        read_only_fields = ["incident_id", "timestamp"]
