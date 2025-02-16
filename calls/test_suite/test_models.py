from django.test import TestCase
from calls.models import Call, CallInteraction

from django.test import TestCase
from calls.models import Call, CallInteraction

class CallModelTest(TestCase):
    def setUp(self):
        """Create a sample call for testing"""
        self.call = Call.objects.create(
            call_sid="12345ABC",
            caller_number="+1234567890",
            location="123 Main St",
            emergency_type="POLICE",
            incident_number="INC001",
            priority_level="HIGH",
            status="ACTIVE"
        )

    def test_call_creation(self):
        """Test if a Call object is created properly"""
        self.assertEqual(self.call.call_sid, "12345ABC")
        self.assertEqual(self.call.caller_number, "+1234567890")
        self.assertEqual(self.call.status, "ACTIVE")

    def test_call_str_representation(self):
        """Test string representation of a Call object"""
        self.assertEqual(str(self.call), "POLICE - +1234567890 - ACTIVE")

class CallInteractionModelTest(TestCase):
    def setUp(self):
        """Create a sample call and interaction"""
        self.call = Call.objects.create(
            call_sid="67890XYZ",
            caller_number="+0987654321",
            location="456 Elm St",
            emergency_type="MEDICAL",
            incident_number="INC002",
            priority_level="MEDIUM",
            status="ACTIVE"
        )
        self.interaction = CallInteraction.objects.create(
            call=self.call,
            speaker="CALLER",
            message="Help, I need an ambulance!"
        )

    def test_interaction_creation(self):
        """Test if a CallInteraction object is created properly"""
        self.assertEqual(self.interaction.call.call_sid, "67890XYZ")
        self.assertEqual(self.interaction.speaker, "CALLER")
        self.assertEqual(self.interaction.message, "Help, I need an ambulance!")
