from django.db import models
from units.models import Unit
from calls.models import Call
from incidents.models import Incident

class Interaction(models.Model):
    SPEAKER_TYPE_CHOICES = [
        ("DISPATCH", "Dispatch"),
        ("UNIT", "Unit"),
    ]

    speaker_type = models.CharField(max_length=20, choices=SPEAKER_TYPE_CHOICES)
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True, related_name="interactions")
    
    call = models.ForeignKey(Call, on_delete=models.CASCADE, related_name="interactions")
    incident = models.ForeignKey(Incident, on_delete=models.SET_NULL, null=True, blank=True, related_name="interactions")

    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.speaker_type == "UNIT" and self.unit:
            return f"{self.unit.identifier}: {self.message[:30]}"
        return f"DISPATCH: {self.message[:30]}"
