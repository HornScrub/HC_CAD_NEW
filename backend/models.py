from django.db import models



class Vehicle(models.Model):
    '''
    license_plate: Should make license_plates a model probably, and embed a function to check license plate validity (per state? county?)
    '''
    license_plate = models.CharField(max_length=10, unique=True) 
    # owner: 
    owner = models.ForeignKey('Person', on_delete=models.CASCADE, null=True, default=None, related_name='vehicles')
    
    address = models.ForeignKey('Address', on_delete=models.SET_NULL, null=True, related_name='vehicles')  # Nullable if no address
    '''
    vehicle_make, vehicle_model : Should standardize inputs (probably all inputs) using save() function eg. input- "Ford " " Focus" -> "FORD" "FOCUS"
    '''
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField(null=True, blank=True)
    color = models.CharField(max_length=20, blank=True, null=True)

    '''
    registration - might need to be a model with all pertinent registration information
    '''
    registration = models.CharField(max_length=20, blank=True, null=True)
    # is_stolen : Should point to a member of an Incident() maybe?
    is_stolen = models.BooleanField(default=False)
    # outstanding warrents: This probably should point to the owner's warrents:
    outstanding_warrants = models.TextField(blank=True, null=True)



    # Use save() to standardize the input before we create the object in the db

    def save(self, *args, **kwargs):
        # Standardize fields
        self.vehicle_make = self.vehicle_make.strip().upper()
        self.vehicle_model = self.vehicle_model.strip().upper()

        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.license_plate
    
class Address(models.Model):
    street = models.CharField(max_length=255, blank=True, null=True)  # e.g., "123 Elm St"
    apartment = models.CharField(max_length=50, blank=True, null=True)  # e.g., "Apt 4B"
    city = models.CharField(max_length=100, blank=True, null=True)  # e.g., "Austin"
    state = models.CharField(max_length=50, blank=True, null=True)  # e.g., "Texas"
    country = models.CharField(max_length=50, default="USA")  # Default to USA
    postal_code = models.CharField(max_length=20, blank=True, null=True)  # e.g., ZIP or international postal code
    owner = models.ForeignKey('Person', on_delete=models.SET_NULL, null=True, blank=True, related_name='addresses') 
    residents = models.ManyToManyField('Person', related_name='residences', blank=True)

    # Use save() to standardize the input before we add the object to db
    def save(self, *args, **kwargs):
        # Standardize text fields
        if self.street:
            self.street = self.street.strip().upper()
        if self.apartment:
            self.apartment = self.apartment.strip().upper()
        if self.city:
            self.city = self.city.strip().upper()
        if self.state:
            self.state = self.state.strip().upper()
        if self.postal_code:
            self.postal_code = self.postal_code.strip().upper()
        super().save(*args, **kwargs)

    def __str__(self):
        address = f"{self.street or 'UNKNOWN'}"
        if self.apartment:
            address += f", {self.apartment}"
        address += f", {self.city or 'UNKNOWN'}, {self.state or 'UNKNOWN'}, {self.country}, {self.postal_code or 'UNKNOWN'}"
        return address

class Person(models.Model):
    
    # Identification
    first_name = models.CharField(max_length=40)
    middle_name = models.CharField(max_length=40, blank=True, null=True)  # could be null for individuals without middle names
    last_name = models.CharField(max_length=40)
    '''
    aliases - could be nicknames, previous legal names, should be expanded
    '''
    aliases = models.TextField(blank=True, null=True)  # Comma-separated or JSON list
    


    # Identification Numbers
    nationality = models.CharField(max_length=50, blank=True, null=True)

    '''
    drivers_license - this should be its own model, person's can have multiple licenses, info on license will contradict stated personal info, etc.
    All these members are just placeholders, need to be elaborated. Might be more members that just this.
    '''

    drivers_license_number = models.CharField(max_length=20, blank=True, null=True)
    drivers_license_address = models.ForeignKey('Address', on_delete=models.SET_NULL, null=True, related_name='license_holders') # Address stated on DL
    drivers_license_first_name = models.CharField(max_length=40, blank=True, null=True)
    drivers_license_middle_name = models.CharField(max_length=40, blank=True, null=True)
    drivers_license_last_name = models.CharField(max_length=40, blank=True, null=True)
    drivers_license_sex = models.CharField(max_length=20, blank=True, null=True)
    drivers_license_gender = models.CharField(max_length=20, blank=True, null=True)
    drivers_license_height = models.IntegerField(blank=True, null=True)
    drivers_license_weight = models.IntegerField(blank=True, null=True)
    drivers_license_eye_color = models.CharField(max_length=20, blank=True, null=True)
    drivers_license_state_issued = models.CharField(max_length=20, blank=True, null=True)
    drivers_license_issue_date = models.CharField(max_length=20, blank=True, null=True) # Issue date of DL
    drivers_license_expiry_date = models.DateField(blank=True, null=True) # Expiration date of DL
    drivers_license_discriminator = models.CharField(max_length=20, blank=True, null=True) # Unique number that identifes driver's license from other documents
    drivers_license_class = models.CharField(max_length=20, blank=True, null=True)
    drivers_license_end_date = models.DateField(blank=True, null=True) # Driver's license endorsements
    drivers_license_rstr = models.CharField(max_length=20, blank=True, null=True) # Driver's license restrictions
    drivers_license_donor = models.CharField(max_length=20, blank=True, null=True) # Organ donor status

    '''
    passport, nationality - need to do research on info contained on a US passport, probably other passports as well. 
    will need to be expanded. Probably needs to be its own model as well. Will we have to create a model per nation, 
    they all have their own rules.
    '''

    passport_number = models.CharField(max_length=20, blank=True, null=True)
    
    # Contact Information

    '''
    email - need to standardize in uppercasing 
    '''

    email_primary = models.EmailField(unique=True)
    email_secondary = models.EmailField(blank=True, null=True)
    
    '''
    Phone_number_primary, type - need to standardize in the (x) (xxx) xxx-xxxx format and uppercasing
    '''
    phone_number_primary = models.CharField(max_length=15, blank=True, null=True)
    phone_number_primary_type = models.CharField(max_length=20, blank=True, null=True) # e.g., "Mobile", "Home", "Work"

    '''
    home_address - we should account for in the event of a non-traditional residential address (homeless, mobile home), either updating 
    Address or doing something else.
    '''

    home_address = models.ForeignKey('Address', on_delete=models.SET_NULL, null=True, related_name='home_residents')
    work_address = models.ForeignKey('Address', on_delete=models.SET_NULL, null=True, related_name='employees')

    # Physical Description
    gender = models.CharField(max_length=20, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], blank=True, null=True)
    '''
    Height, weight - should decide between imperial vs metric, leaning imperial, maybe should be TextField for appended lbs/feet, inches
    '''
    height = models.IntegerField(blank=True, null=True)  # in cm
    weight = models.IntegerField(blank=True, null=True)  # in kg
    eye_color = models.CharField(max_length=20, blank=True, null=True)
    '''
    distinguishing_features - catch all for tattoos, marks, piercings, scars, burns, augmentations, etc., could be expanded to include limbless, extreme height/size, stuff like that
    '''
    has_distinguishing_features = models.BooleanField(default=False)
    distinguishing_features = models.TextField(blank=True, null=True)

    # Personal Information
    date_of_birth = models.DateField()
    occupation = models.CharField(max_length=100, blank=True, null=True)
    employer = models.CharField(max_length=100, blank=True, null=True)

    '''
    employer_person - could be supervisor, could expand to coworkers, subordinates, etc.
    '''
    employer_person = models.ForeignKey('Person', on_delete=models.SET_NULL, null=True, related_name='employee')
    employer_address = models.ForeignKey('Address', on_delete=models.SET_NULL, null=True, related_name='employee_address')

    '''
    vehicles_owned - should be vehicles currently registered in their name, should make something for past vehicles owned. Theres
    
    '''

    vehicles_owned = models.ManyToManyField('Vehicle', related_name='owners', blank=True)

    # Medical Information

    '''
    is_5150 - should describe someone gravely disabled through mental illness, not sure the right term for this
    '''
    is_5150 = models.BooleanField(default=False)
    '''
    medical_conditions - catch-all for any medical conditions from allergy to visable disability, probably should be expanded to seperate the two
    '''

    medical_conditions = models.TextField(blank=True, null=True)
    '''
    mental_health_history - catch-all for any mental health history, ambigious right now if this could point to LEO incidents or caller provided info, etc.
    '''
    mental_health_history = models.TextField(blank=True, null=True)
    
    '''
    Associations - I think its important to have reports of associations for LEO investigation, but I'm not sure if I should have explicit relationships here
    or relationships through incidents, etc. Makes sense for me right now to make the relationships explicit
    Associations could be anything to family, friends, roomates, coworkers, crime partners, addresses, vehicles, incidents, etc. Needs to be
    expanded'''
    
    #Associations

    ## Familial Relationships
    family_of = models.ManyToManyField('Person', related_name='family_members', blank=True) # Should catch cousins, aunts/uncles, or maybe its redundant
    spouse_of = models.ManyToManyField('Person', related_name='spouses', blank=True)
    parent_of = models.ManyToManyField('Person', related_name='children', blank=True)
    sibling_of = models.ManyToManyField('Person', related_name='siblings', blank=True)
    child_of = models.ManyToManyField('Person', related_name='parents', blank=True)
    grandparent_of = models.ManyToManyField('Person', related_name='grandchildren', blank=True)
    grandchild_of = models.ManyToManyField('Person', related_name='grandparents', blank=True)

    ## Social Relationships
    friends_with = models.ManyToManyField('Person', related_name='friends', blank=True)
    roommates_with = models.ManyToManyField('Person', related_name='roommates', blank=True)
    coworkers_with = models.ManyToManyField('Person', related_name='coworkers', blank=True)
    acquaintances_with = models.ManyToManyField('Person', related_name='acquaintances', blank=True)
    '''
    group_member_of - Might want to include their social groups and functions, agnostic to criminality for now (could be criminal gang or benign club)
    '''
    # group_member_of = models.ManyToManyField('TextField', related_name='groups', blank=True)

    ## General Associations
    phone_number_associated = models.CharField(max_length=15, blank=True, null=True)
    addresses_associated = models.ManyToManyField('Address', related_name='associated_residents', blank=True)
    vehicles_associated = models.ManyToManyField('Vehicle', related_name='associated_people', blank=True)
    persons_associated = models.ManyToManyField('Person', related_name='associated_persons', blank=True)

    '''
    incidents_associated - I'd want this to represent incidents they aren't the primary subject of, eg. made the emergency call,
    gave testimony, that sort of thing
    '''
    # incidents_associated = models.ManyToManyField('Incident', related_name='incidents_associated', blank=True)

    # Criminality

    has_active_warrants = models.BooleanField(default=False)
    active_warrants = models.TextField(blank=True, null=True)
    warrant_history = models.TextField(blank=True, null=True)

    on_probation = models.BooleanField(default=False)
    parole_officer = models.ForeignKey('Person', on_delete=models.SET_NULL, null=True, related_name='parolees')

    has_criminal_history = models.BooleanField(default=False, null=True)
    criminal_history_primary = models.TextField(blank=True, null=True)


