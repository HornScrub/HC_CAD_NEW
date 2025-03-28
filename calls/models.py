from django.db import models
from units.models import Unit  # Import Unit model

class Call(models.Model):
    call_sid = models.CharField(max_length=100, unique=True)  # Twilio or internal ID
    call_id = models.CharField(max_length=100, editable=False, null=True, blank=True)  # Human-friendly ID
    caller_number = models.CharField(max_length=20)
    incident = models.ForeignKey("incidents.Incident", on_delete=models.SET_NULL, null=True, blank=True, related_name="calls")

    timestamp = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    duration_seconds = models.PositiveIntegerField(null=True, blank=True)

    def complete_call(self):
        from django.utils.timezone import now
        self.completed_at = now()
        if self.timestamp:
            self.duration_seconds = (self.completed_at - self.timestamp).total_seconds()
        self.save()

    def save(self, *args, **kwargs):
        if not self.call_id:
            count = Call.objects.count() + 1
            short_number = ''.join(filter(str.isdigit, self.caller_number))[-4:] or "0000"
            self.call_id = f"CALL-{count:04d}-{short_number}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.call_id or self.call_sid


