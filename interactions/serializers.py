from rest_framework import serializers
from .models import Interaction
from units.models import Unit

class InteractionSerializer(serializers.ModelSerializer):
    # Accepts unit by identifier (e.g., "21B")
    unit = serializers.SlugRelatedField(
        queryset=Unit.objects.all(),
        slug_field="identifier",
        allow_null=True,
        required=False
    )

    class Meta:
        model = Interaction
        fields = [
            "id",
            "speaker_type",
            "unit",
            "call",
            "incident",
            "message",
            "timestamp"
        ]
        read_only_fields = ["id", "timestamp"]
