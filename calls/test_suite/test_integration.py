from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User

class AIDispatcherIntegrationTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create a test user and authenticate
        self.user = User.objects.create_user(username="testuser", password="password123")
        response = self.client.post(reverse("token_obtain_pair"), {"username": "testuser", "password": "password123"}, format="json")
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def test_ai_dispatcher_call_creation(self):
        """Simulates AI Dispatcher sending a new call"""
        response = self.client.post(reverse("call-create"), data={
            "call_sid": "AI001",
            "caller_number": "+18005551234",
            "location": "200 Broadway",
            "emergency_type": "MEDICAL",
            "incident_number": "INC006",
            "priority_level": "HIGH",
            "status": "ACTIVE"
        }, format="json")  # Ensure it's sent as JSON

        print("Response status:", response.status_code)
        print("Response data:", getattr(response, "data", response.content))  # Handles missing response.data

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_ai_dispatcher_logs_interaction(self):
        """Simulates AI Dispatcher logging an interaction"""

        # Ensure call exists before logging interaction
        create_response = self.client.post(reverse("call-create"), data={
            "call_sid": "AI001",
            "caller_number": "+18005551234",
            "location": "200 Broadway",
            "emergency_type": "MEDICAL",
            "incident_number": "INC006",
            "priority_level": "HIGH",
            "status": "ACTIVE"
        }, format="json")

        print("Create Call Response:", create_response.status_code, create_response.data)

        # Ensure call creation was successful before proceeding
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)

        # Now log the interaction
        response = self.client.post(reverse("call-interaction", kwargs={"call_sid": "AI001"}), data={
            "speaker": "SYSTEM",
            "message": "Help is on the way."
        }, format="json")

        print("Response status:", response.status_code)
        print("Response data:", getattr(response, "data", response.content))  # Handles missing response.data

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
