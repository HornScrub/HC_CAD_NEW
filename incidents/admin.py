from django.contrib import admin
from .models import Incident, TrafficStop

@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = ("incident_id", "title", "status", "priority_level", "created_at")
    list_filter = ("status", "priority_level", "emergency_type")
    search_fields = ("incident_id", "title")

@admin.register(TrafficStop)
class TrafficStopAdmin(admin.ModelAdmin):
    list_display = ("officer", "subject", "vehicle", "citation_issued", "timestamp")
    list_filter = ("citation_issued",)
