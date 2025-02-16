from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from calls.models import Call, CallInteraction

class CallAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create a test user and authenticate
        self.user = User.objects.create_user(username="testuser", password="password123")
        response = self.client.post(reverse("token_obtain_pair"), {"username": "testuser", "password": "password123"}, format="json")
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")  # Set token in headers

        # Create a sample call
        self.call = Call.objects.create(
            call_sid="12345TEST",
            caller_number="+1555000111",
            location="789 Oak St",
            emergency_type="POLICE",
            incident_number="INC003",
            priority_level="HIGH",
            status="ACTIVE"
        )

    def test_create_call(self):
        """Test creating a new call"""
        response = self.client.post(reverse("call-create"), {
            "call_sid": "54321NEW",
            "caller_number": "+1666777888",
            "location": "101 Pine St",
            "emergency_type": "MEDICAL",
            "incident_number": "INC004",
            "priority_level": "MEDIUM",
            "status": "ACTIVE"
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Call.objects.count(), 2)  # One existing, one new

    def test_get_call(self):
        """Test retrieving an existing call"""
        response = self.client.get(reverse("call-update", kwargs={"call_sid": "12345TEST"}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["caller_number"], "+1555000111")

    def test_update_call(self):
        """Test updating an existing call"""
        response = self.client.put(reverse("call-update", kwargs={"call_sid": "12345TEST"}), {
            "status": "COMPLETED"
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.call.refresh_from_db()
        self.assertEqual(self.call.status, "COMPLETED")

class CallInteractionAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create a test user and authenticate
        self.user = User.objects.create_user(username="testuser", password="password123")
        response = self.client.post(reverse("token_obtain_pair"), {"username": "testuser", "password": "password123"}, format="json")
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

        # Create a sample call
        self.call = Call.objects.create(
            call_sid="INTERACT123",
            caller_number="+1999888777",
            location="222 Maple St",
            emergency_type="POLICE",
            incident_number="INC005",
            priority_level="LOW",
            status="ACTIVE"
        )

    def test_create_interaction(self):
        """Test logging a new interaction"""
        response = self.client.post(reverse("call-interaction", kwargs={"call_sid": "INTERACT123"}), {
            "speaker": "CALLER",
            "message": "This is a test message."
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CallInteraction.objects.count(), 1)

