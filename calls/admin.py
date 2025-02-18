from django.contrib import admin
from django.http import HttpResponse
import csv
from .models import Call, CallInteraction

# Function to export selected calls as CSV
def export_calls_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="calls_export.csv"'
    writer = csv.writer(response)

    # Write CSV headers
    writer.writerow(["Incident Number", "Caller Number", "Emergency Type", "Status", "Priority Level", "Timestamp", "Completed At"])

    # Write row data
    for call in queryset:
        writer.writerow([
            call.incident_number,
            call.caller_number,
            call.emergency_type,
            call.status,
            call.priority_level,
            call.timestamp,  # FIX: Changed from created_at to timestamp
            call.completed_at if call.completed_at else "N/A"
        ])
    
    return response

export_calls_csv.short_description = "Export Selected Calls as CSV"

@admin.register(Call)
class CallAdmin(admin.ModelAdmin):
    list_display = ("incident_number", "caller_number", "emergency_type", "status", "priority_level", "timestamp")  # FIX
    list_filter = ("status", "emergency_type", "priority_level")
    search_fields = ("incident_number", "caller_number")
    
    actions = [export_calls_csv]  # Add CSV export action
    
    actions_on_top = True  # Show actions dropdown at the top
    actions_on_bottom = True  # Show actions dropdown at the bottom

@admin.register(CallInteraction)
class CallInteractionAdmin(admin.ModelAdmin):
    list_display = ("call", "speaker", "timestamp")
    search_fields = ("call__incident_number", "text")  # FIX: Changed "message" to "text"
