from django.contrib import admin
from .models import Vehicle, Address, Person

# Register your models here.

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('license_plate', 'owner', 'make', 'model', 'is_stolen')
    search_fields = ('license_plate', 'owner', 'vmake', 'model')

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('street', 'apartment', 'city', 'country', 'postal_code', 'owner')
    search_fields = ('street', 'apartment', 'city', 'country', 'postal_code', 'owner')

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'middle_name', 'last_name', 'drivers_license_number', 'passport_number', 'email_primary', 'phone_number_primary', 'home_address', 'work_address', 'date_of_birth')
    search_fields = ('first_name', 'middle_name', 'last_name', 'drivers_license_number', 'passport_number', 'email_primary', 'phone_number_primary', 'home_address', 'work_address', 'date_of_birth')