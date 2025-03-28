from django.contrib import admin
from .models import Interaction

@admin.register(Interaction)
class InteractionAdmin(admin.ModelAdmin):
    list_display = ("speaker_type", "unit", "call", "incident", "timestamp")
    list_filter = ("speaker_type", "timestamp")
    search_fields = ("message",)
