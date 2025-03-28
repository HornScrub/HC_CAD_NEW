from django.db import models

STATUS_CHOICES = [
    ("10-8", "In Service"),
    ("10-7", "Out of Service"),
    ("10-6", "Busy"),
    ("10-11", "Traffic Stop"),
    ("10-97", "On Scene"),
    ("10-23", "Arrived at Location"),
    ("10-19", "Returning to Station"),
]

class Unit(models.Model):
    identifier = models.CharField(max_length=10, unique=True)  # like A1, M2
    name = models.CharField(max_length=50)  # Optional: “Officer Smith”
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="10-8")
    current_call = models.ForeignKey("calls.Call", null=True, blank=True, on_delete=models.SET_NULL)
    location = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.identifier} - {self.name or 'Unnamed'}"
