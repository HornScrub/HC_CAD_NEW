from rest_framework import serializers
from .models import Vehicle, Subject, DriversLicense, Address

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'

class SubjectSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = [
            "id",
            "first_name",
            "last_name",
            "date_of_birth",
            "gender",
            "eye_color",
            "height_cm",
            "weight_kg",
            "phone_number_primary",
            "home_address",
        ]

class SubjectDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class DriversLicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriversLicense
        fields = '__all__'

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "id",
            "street",
            "apartment",
            "city",
            "state",
            "country",
            "postal_code",
            "owner",
            "residents",
        ]
        read_only_fields = ["id"]