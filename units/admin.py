from django.contrib import admin
from .models import Unit

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ("identifier", "name", "status", "location", "is_active", "last_updated")
    search_fields = ("identifier", "name")
    list_filter = ("status", "is_active")
