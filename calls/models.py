from django.db import models

class Call(models.Model):
    call_sid = models.CharField(max_length=100, unique=True)  # Twilio Call ID
    caller_number = models.CharField(max_length=20)
    category = models.CharField(max_length=50, default="GENERAL", blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    emergency_type = models.CharField(
        max_length=50, choices=[("POLICE", "Police"), ("MEDICAL", "Medical")],
        blank=True, null=True
    )
    incident_number = models.CharField(max_length=50, unique=True, blank=True, null=True)
    priority_level = models.CharField(
        max_length=20, choices=[("STANDARD", "Standard"), ("MEDIUM", "Medium"), ("HIGH", "High")],
        blank=True, null=True
    )
    
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("ACTIVE", "Active"),
        ("DISPATCHED", "Dispatched"),
        ("ESCALATED", "Escalated"),
        ("COMPLETED", "Completed"),
        ("CANCELLED", "Cancelled"),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")

    timestamp = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    duration_seconds = models.PositiveIntegerField(null=True, blank=True)  # Call duration in seconds

    escalated_to_911 = models.BooleanField(default=False)
    units_dispatched = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.emergency_type} - {self.caller_number} - {self.status}"

    def complete_call(self):
        """Mark the call as completed and store duration."""
        from django.utils.timezone import now  # Ensure timezone awareness
        self.completed_at = now()
        if self.timestamp:
            self.duration_seconds = (self.completed_at - self.timestamp).total_seconds()
        self.save()



class CallInteraction(models.Model):
    call = models.ForeignKey(Call, on_delete=models.CASCADE, related_name="interactions")

    SPEAKER_CHOICES = [("CALLER", "Caller"), ("DISPATCHER", "Dispatcher")]
    speaker = models.CharField(max_length=20, choices=SPEAKER_CHOICES)

    message = models.TextField(blank=True, null=True)  # ✅ Allow updates later
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.speaker}: {self.message[:50]}" if self.message else f"{self.speaker}: (No message yet)"




