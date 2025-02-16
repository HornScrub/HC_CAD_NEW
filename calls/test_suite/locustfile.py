from locust import HttpUser, task, between
import random
import string

class DispatcherLoadTest(HttpUser):
    wait_time = between(1, 3)  # Simulate real-world delays
    host = "http://127.0.0.1:8000"
    token = None  # Store authentication token

    def on_start(self):
        """Log in and retrieve JWT token when a new user starts"""
        response = self.client.post("/api/token/", json={
            "username": "test1",
            "password": "whateveryouwant"
        })
        if response.status_code == 200:
            self.token = response.json()["access"]  # Save the token
        else:
            print("Authentication failed:", response.text)

    def generate_sid(self):
        """Generate a unique call_sid"""
        return "CALL_" + "".join(random.choices(string.ascii_uppercase + string.digits, k=8))

    def random_phone(self):
        """Generate a random caller number"""
        return "+1" + "".join(random.choices(string.digits, k=10))

    def random_location(self):
        """Pick a random location"""
        locations = [
            "100 Main St", "500 Elm St", "200 Broadway", "321 Oak St",
            "75 River Rd", "420 Maple Ave", "10 Pine Blvd"
        ]
        return random.choice(locations)

    def random_emergency_type(self):
        """Pick a random emergency type"""
        return random.choice(["POLICE", "MEDICAL", "FIRE"])

    def random_priority(self):
        """Pick a random priority level"""
        return random.choice(["LOW", "MEDIUM", "HIGH", "CRITICAL"])

    def random_status(self):
        """Pick a random status"""
        return random.choice(["ACTIVE", "IN_PROGRESS", "COMPLETED", "CANCELLED"])

    @task(3)  # Call creation is 3x more frequent
    def create_call(self):
        """Simulate AI Dispatcher creating a call"""
        if not self.token:
            print("Skipping request due to missing token.")
            return

        headers = {"Authorization": f"Bearer {self.token}"}
        call_sid = self.generate_sid()

        response = self.client.post("/api/calls/", json={
            "call_sid": call_sid,
            "caller_number": self.random_phone(),
            "location": self.random_location(),
            "emergency_type": self.random_emergency_type(),
            "incident_number": call_sid,  # Using SID as incident number for uniqueness
            "priority_level": self.random_priority(),
            "status": self.random_status()
        }, headers=headers)

        if response.status_code != 201:
            print(f"Create Call Failed [{response.status_code}]: {response.text}")

    @task(1)  # Interaction logging is less frequent
    def log_interaction(self):
        """Simulate AI Dispatcher logging interactions"""
        if not self.token:
            print("Skipping request due to missing token.")
            return

        headers = {"Authorization": f"Bearer {self.token}"}

        # Pick a random call SID that was previously generated
        call_sid = self.generate_sid()

        response = self.client.post(f"/api/calls/{call_sid}/interactions/", json={
            "speaker": "SYSTEM",
            "message": "Emergency responders are en route."
        }, headers=headers)

        if response.status_code != 201:
            print(f"Log Interaction Failed [{response.status_code}]: {response.text}")


