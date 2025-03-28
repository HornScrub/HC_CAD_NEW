from django.db import models
from units.models import Unit
from calls.models import Call
import uuid

def generate_subject_uid():
    return f"SBJ-{uuid.uuid4().hex[:8].upper()}"

class Subject(models.Model):
    subject_uid = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        default=generate_subject_uid
    )   
    # Identification
    first_name = models.CharField(max_length=40)
    middle_name = models.CharField(max_length=40, blank=True, null=True)
    last_name = models.CharField(max_length=40)
    aliases = models.JSONField(blank=True, null=True)  # Stores nicknames/aliases as a list

    # Identity Links
    drivers_license = models.ForeignKey('DriversLicense', on_delete=models.SET_NULL, null=True, blank=True, related_name='subjects')
    passport_number = models.CharField(max_length=20, blank=True, null=True)

    # Contact Info
    email_primary = models.EmailField(unique=True, blank=True, null=True)
    email_secondary = models.EmailField(blank=True, null=True)
    phone_number_primary = models.CharField(max_length=15, blank=True, null=True)
    phone_number_primary_type = models.CharField(max_length=20, blank=True, null=True)
    home_address = models.ForeignKey('Address', on_delete=models.SET_NULL, null=True, blank=True, related_name='home_residents')
    work_address = models.ForeignKey('Address', on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')

    # Physical Description
    gender = models.CharField(max_length=20, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], blank=True, null=True)
    height_cm = models.IntegerField(blank=True, null=True, verbose_name="Height (cm)")
    weight_kg = models.IntegerField(blank=True, null=True, verbose_name="Weight (kg)")
    eye_color = models.CharField(max_length=20, blank=True, null=True)
    has_distinguishing_features = models.BooleanField(default=False)
    distinguishing_features = models.TextField(blank=True, null=True)

    # Personal Info
    date_of_birth = models.DateField()
    occupation = models.CharField(max_length=100, blank=True, null=True)
    employer = models.CharField(max_length=100, blank=True, null=True)
    employer_person = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, related_name='employee')
    employer_address = models.ForeignKey('Address', on_delete=models.SET_NULL, null=True, related_name='employee_address')
    vehicles_owned = models.ManyToManyField('Vehicle', related_name='owners', blank=True)

    # Medical Info
    is_5150 = models.BooleanField(default=False)
    medical_conditions = models.TextField(blank=True, null=True)
    mental_health_history = models.TextField(blank=True, null=True)

    # Relationships
    family_of = models.ManyToManyField('self', symmetrical=False, related_name='family_members', blank=True)
    spouse_of = models.ManyToManyField('self', symmetrical=True, related_name='spouses', blank=True)
    parent_of = models.ManyToManyField('self', symmetrical=False, related_name='children', blank=True)
    child_of = models.ManyToManyField('self', symmetrical=False, related_name='parents', blank=True)
    grandparent_of = models.ManyToManyField('self', symmetrical=False, related_name='grandchildren', blank=True)
    grandchild_of = models.ManyToManyField('self', symmetrical=False, related_name='grandparents', blank=True)
    sibling_of = models.ManyToManyField('self', symmetrical=True, related_name='siblings', blank=True)
    friends_with = models.ManyToManyField('self', symmetrical=True, related_name='friends', blank=True)
    roommates_with = models.ManyToManyField('self', symmetrical=True, related_name='roommates', blank=True)
    coworkers_with = models.ManyToManyField('self', symmetrical=True, related_name='coworkers', blank=True)
    acquaintances_with = models.ManyToManyField('self', symmetrical=True, related_name='acquaintances', blank=True)

    phone_number_associated = models.CharField(max_length=15, blank=True, null=True)
    addresses_associated = models.ManyToManyField('Address', related_name='associated_residents', blank=True)
    vehicles_associated = models.ManyToManyField('Vehicle', related_name='associated_people', blank=True)
    persons_associated = models.ManyToManyField('self', related_name='associated_persons', blank=True)

    # Criminal Info
    has_active_warrants = models.BooleanField(default=False)
    active_warrants = models.TextField(blank=True, null=True)
    warrant_history = models.TextField(blank=True, null=True)
    on_probation = models.BooleanField(default=False)
    parole_officer = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, related_name='parolees')
    has_criminal_history = models.BooleanField(default=False, null=True)
    criminal_history_primary = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Vehicle(models.Model):
    license_plate = models.CharField(max_length=10, unique=True)

    owner = models.ForeignKey('Subject', on_delete=models.SET_NULL, null=True, blank=True, default=None, related_name='vehicles')
    address = models.ForeignKey('Address', on_delete=models.SET_NULL, null=True, blank=True, related_name='vehicles')

    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField(null=True, blank=True)
    color = models.CharField(max_length=20, blank=True, null=True)

    registration = models.CharField(max_length=20, blank=True, null=True)
    is_stolen = models.BooleanField(default=False)
    outstanding_warrants = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.make = self.make.strip().upper()
        self.model = self.model.strip().upper()
        self.license_plate = self.license_plate.strip().upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.license_plate

class Address(models.Model):
    street = models.CharField(max_length=255, blank=True, null=True)  # e.g., "123 Elm St"
    apartment = models.CharField(max_length=50, blank=True, null=True)  # e.g., "Apt 4B"
    city = models.CharField(max_length=100, blank=True, null=True)  # e.g., "Austin"
    state = models.CharField(max_length=50, blank=True, null=True)  # e.g., "TX"
    country = models.CharField(max_length=50, default="USA")  # Assume USA unless otherwise specified
    postal_code = models.CharField(max_length=20, blank=True, null=True)  # ZIP or other

    # Associations
    owner = models.ForeignKey(
        "Subject", on_delete=models.SET_NULL, null=True, blank=True, related_name="addresses"
    )
    residents = models.ManyToManyField(
        "Subject", related_name="residences", blank=True
    )

    def save(self, *args, **kwargs):
        """Standardize string fields before saving."""
        for field in ["street", "apartment", "city", "state", "postal_code", "country"]:
            value = getattr(self, field, None)
            if value:
                setattr(self, field, value.strip().upper())
        super().save(*args, **kwargs)

    def __str__(self):
        parts = [self.street, self.apartment, self.city, self.state, self.country, self.postal_code]
        parts_clean = [p for p in parts if p]
        return ", ".join(parts_clean) if parts_clean else "UNKNOWN ADDRESS"

class DriversLicense(models.Model):
    subject = models.ForeignKey("Subject", on_delete=models.SET_NULL, null=True, blank=True, related_name="drivers_licenses")


    # License Info
    license_number = models.CharField(max_length=20, unique=True)
    address_on_license = models.ForeignKey(
        "Address", on_delete=models.SET_NULL, null=True, related_name="license_holders"
    )

    state_issued = models.CharField(max_length=20, blank=True, null=True)
    issue_date = models.CharField(max_length=20, blank=True, null=True)  # Consider DateField if format consistent
    expiry_date = models.DateField(blank=True, null=True)
    discriminator = models.CharField(max_length=20, blank=True, null=True)  # Optional unique backend ID
    license_class = models.CharField(max_length=20, blank=True, null=True)
    endorsement_date = models.DateField(blank=True, null=True)
    restriction = models.CharField(max_length=20, blank=True, null=True)
    organ_donor = models.BooleanField(default=False)

    # Name (may differ from Subject)
    first_name = models.CharField(max_length=40, blank=True, null=True)
    middle_name = models.CharField(max_length=40, blank=True, null=True)
    last_name = models.CharField(max_length=40, blank=True, null=True)

    # Physical description
    sex = models.CharField(max_length=20, blank=True, null=True)  # May be different than gender
    gender = models.CharField(max_length=20, blank=True, null=True)
    height_cm = models.IntegerField(blank=True, null=True)
    weight_kg = models.IntegerField(blank=True, null=True)
    eye_color = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.license_number} ({self.state_issued})"


