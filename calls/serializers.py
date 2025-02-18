from rest_framework import serializers
from .models import Call, CallInteraction

class CallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Call
        fields = '__all__'

class CallInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallInteraction
        fields = '__all__'
