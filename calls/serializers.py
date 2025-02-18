from rest_framework import serializers
from .models import Call, CallInteraction

class CallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Call
        fields = '__all__'
        extra_kwargs = {
            "location": {"required": False},  # Now optional
            "emergency_type": {"required": False},
            "incident_number": {"required": False},
            "priority_level": {"required": False},
        }

class CallInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallInteraction
        fields = '__all__'
