from django.contrib import admin
from .models import Subject, Vehicle, Address, DriversLicense

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("subject_uid", "first_name", "last_name", "date_of_birth", "has_criminal_history")
    search_fields = ("first_name", "last_name", "subject_uid")
    list_filter = ("has_criminal_history", "has_active_warrants", "gender")

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ("license_plate", "make", "model", "year", "is_stolen")
    search_fields = ("license_plate", "make", "model")
    list_filter = ("is_stolen",)

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("__str__", "city", "state", "country")
    search_fields = ("street", "city", "state", "postal_code")

@admin.register(DriversLicense)
class DriversLicenseAdmin(admin.ModelAdmin):
    list_display = ("license_number", "state_issued", "expiry_date", "organ_donor")
    search_fields = ("license_number", "first_name", "last_name")
    list_filter = ("organ_donor", "state_issued")

