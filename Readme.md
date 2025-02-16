Create Django Backend for AI Emergency Dispatch System Integration
Overview
Create a Django backend application to integrate with our existing AI Emergency Dispatch System (ref: [GitHub URL]). This backend will handle call logging, provide an admin interface, and store call data from our Twilio-based dispatch system.
Objectives

Set up Django project structure
Create database models for call tracking
Implement API endpoints for AI dispatcher integration
Create admin interface for call management
Implement call logging and analytics

Technical Requirements
Environment Setup
bashCopy# Create virtual environment
python -m venv env
source env/bin/activate

# Install dependencies
pip install django djangorestframework django-environ psycopg2-binary
Project Structure
Copydispatch_backend/
├── manage.py
├── requirements.txt
├── .env
├── dispatch/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── calls/
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── admin.py
    └── urls.py
Database 

How to Switch Between Test and Real Databases
Switch to Test DB

Run this before starting Django:

export USE_TEST_DB=True
python manage.py runserver
(For Windows, use set USE_TEST_DB=True)

2) Switch Back to Real DB

export USE_TEST_DB=False
python manage.py runserver

Or update your .env file:

# Use test database
USE_TEST_DB=True

Then restart Django:

python manage.py runserver
How to Verify Which Database is Active

Run:
python manage.py dbshell

Then check:

SELECT current_database();
If it shows dispatch_db → You're in production DB.
If it shows dispatch_test_db → You're in test DB.

Models

In calls/models.py:
pythonCopyclass Call(models.Model):
    call_sid = models.CharField(max_length=100, unique=True)
    caller_number = models.CharField(max_length=20)
    location = models.TextField()
    emergency_type = models.CharField(max_length=50)  # POLICE/MEDICAL
    incident_number = models.CharField(max_length=50)
    priority_level = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20)

class CallInteraction(models.Model):
    call = models.ForeignKey(Call, on_delete=models.CASCADE)
    speaker = models.CharField(max_length=20)  # CALLER/SYSTEM
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


API Endpoints Required

Call Creation

POST /api/calls/
Creates new call record when dispatch starts


Call Update

PUT /api/calls/<call_sid>/
Updates call status and details


Interaction Logging

POST /api/calls/<call_sid>/interactions/
Logs each conversation interaction



Admin Interface Requirements
Must implement Django admin interface with:

Call listing with filters (date, type, status)
Detailed call view with interactions
Export functionality for call data

Integration Steps

Database Setup

bashCopy

python manage.py makemigrations
python manage.py migrate

Create Superuser

bashCopypython manage.py createsuperuser

API Integration Example

pythonCopy# In AI dispatcher after call initialization
response = requests.post(
    'http://your-django-backend/api/calls/',
    json={
        'call_sid': call_sid,
        'caller_number': caller_number,
        'emergency_type': emergency_type
    }
)
Testing Requirements

Unit tests for models and API endpoints
Integration tests for AI dispatcher communication
Load testing for concurrent call handling

Acceptance Criteria

Backend successfully receives and stores call data
Admin interface displays all call information
API endpoints handle all AI dispatcher requests
Call interactions are properly logged and timestamped
System handles concurrent calls without issues

Security Requirements

Implement API authentication
Secure sensitive caller information
Add request rate limiting
Implement proper CORS settings

Documentation Needed

API documentation
Database schema documentation
Setup and deployment instructions
Admin interface user guide

Timeline

Environment Setup: 1 day
Database Models: 1 day
API Endpoints: 2 days
Admin Interface: 1 day
Testing: 2 days
Documentation: 1 day

Total Estimated Time: 8 days
Priority
High - Required for production deployment of AI dispatcher system
Dependencies

Access to AI dispatcher codebase
Twilio account credentials
Production server access

Note: The AI dispatcher is already developed and working. This ticket is specifically for creating the Django backend that will store and manage the call data. The backend needs to integrate with our existing AI system which handles the actual calls.