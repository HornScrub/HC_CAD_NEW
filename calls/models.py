from django.db import models

class Call(models.Model):
    call_sid = models.CharField(max_length=100, unique=True)  # Twilio Call ID
    caller_number = models.CharField(max_length=20)
    location = models.TextField()
    emergency_type = models.CharField(max_length=50, choices=[("POLICE", "Police"), ("MEDICAL", "Medical")])
    incident_number = models.CharField(max_length=50, unique=True)
    priority_level = models.CharField(max_length=20, choices=[("LOW", "Low"), ("MEDIUM", "Medium"), ("HIGH", "High")])
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[("ACTIVE", "Active"), ("COMPLETED", "Completed"), ("CANCELLED", "Cancelled")])

    def __str__(self):
        return f"{self.emergency_type} - {self.caller_number} - {self.status}"

class CallInteraction(models.Model):
    call = models.ForeignKey(Call, on_delete=models.CASCADE, related_name="interactions")
    speaker = models.CharField(max_length=20, choices=[("CALLER", "Caller"), ("SYSTEM", "System")])
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.speaker}: {self.message[:50]}"  # Show first 50 chars

