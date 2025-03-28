from django.contrib import admin
from django.http import HttpResponse
import csv
from .models import Call
from interactions.models import Interaction


# Inline view for Interactions related to a Call
class InteractionInline(admin.TabularInline):
    model = Interaction
    fields = ("speaker_type", "unit", "message", "timestamp")
    readonly_fields = ("speaker_type", "unit", "message", "timestamp")
    extra = 0
    can_delete = False


# Function to export selected calls as CSV
def export_calls_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="calls_export.csv"'
    writer = csv.writer(response)

    writer.writerow([
        "Incident ID", "Caller Number", "Emergency Type",
        "Status", "Priority Level", "Timestamp", "Completed At"
    ])

    for call in queryset:
        incident = call.incident
        writer.writerow([
            incident.incident_id if incident else "N/A",
            call.caller_number,
            incident.emergency_type if incident else "N/A",
            incident.status if incident else "N/A",
            incident.priority_level if incident else "N/A",
            call.timestamp,
            call.completed_at if call.completed_at else "N/A"
        ])
    return response

export_calls_csv.short_description = "Export Selected Calls as CSV"


@admin.register(Call)
class CallAdmin(admin.ModelAdmin):
    list_display = ("call_sid", "caller_number", "get_incident_status", "timestamp", "completed_at")
    search_fields = ("call_sid", "caller_number")
    inlines = [InteractionInline]
    actions = [export_calls_csv]

    def get_incident_status(self, obj):
        return obj.incident.status if obj.incident else "N/A"
    get_incident_status.short_description = "Incident Status"
