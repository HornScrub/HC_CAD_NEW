from django.db import models
from units.models import Unit
from records.models import Subject, Vehicle, Call

class Incident(models.Model):
    incident_id = models.CharField(max_length=50, unique=True, editable=False)
    title = models.CharField(max_length=100, default="Untitled Incident")
    emergency_type = models.CharField(
        max_length=50,
        choices=[("POLICE", "Police"), ("MEDICAL", "Medical")],
        blank=True,
        null=True
    )
    location = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ("OPEN", "Open"),
            ("ACTIVE", "Active"),
            ("RESOLVED", "Resolved"),
            ("ESCALATED", "Escalated"),
            ("CANCELLED", "Cancelled"),
        ],
        default="OPEN"
    )
    priority_level = models.CharField(
        max_length=20,
        choices=[
            ("STANDARD", "Standard"),
            ("MEDIUM", "Medium"),
            ("HIGH", "High")
        ],
        blank=True,
        null=True
    )
    assigned_units = models.ManyToManyField(Unit, blank=True, related_name="incidents")
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Auto-generate ID if not set
        if not self.incident_id:
            last = Incident.objects.order_by("-id").first()
            next_number = 1 if not last else last.id + 1
            self.incident_id = f"INC-{next_number:05d}"  # e.g. INC-00023
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.incident_id} - {self.emergency_type} - {self.status}"

class TrafficStop(Incident):
    officer = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True)
    call = models.ForeignKey(Call, on_delete=models.SET_NULL, null=True, blank=True)
    reason = models.TextField()
    outcome = models.TextField()
    citation_issued = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
