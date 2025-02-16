import os
from locust import HttpUser, task, between
import random
import string

class DispatcherLoadTest(HttpUser):
    wait_time = between(1, 3)
    host = "http://127.0.0.1:8000"
    token = None  
    created_calls = []  # Store created calls to avoid 404 errors

    def on_start(self):
        """Ensure the test database is in use before running tests"""
        if os.getenv("USE_TEST_DB", "False") != "True":
            raise RuntimeError("Switch to the test database before running this test! Set USE_TEST_DB=True.")

        """Log in and retrieve JWT token"""
        response = self.client.post("/api/token/", json={
            "username": "test1",
            "password": "whateveryouwant"
        })
        if response.status_code == 200:
            self.token = response.json()["access"]
        else:
            print("Authentication failed:", response.text)

    def generate_call_sid(self):
        """Generate a unique Call SID (CALL followed by 5 digits)"""
        return "CALL" + "".join(random.choices(string.digits, k=5))

    def generate_incident_number(self):
        """Generate a unique Incident Number (INC followed by 5 digits)"""
        return "INC" + "".join(random.choices(string.digits, k=5))

    @task(3)
    def create_call(self):
        """Create calls and store valid SIDs"""
        if not self.token:
            return

        headers = {"Authorization": f"Bearer {self.token}"}
        call_sid = self.generate_call_sid()
        incident_number = self.generate_incident_number()  # Now different from call_sid

        response = self.client.post("/api/calls/", json={
            "call_sid": call_sid,
            "caller_number": "+1" + "".join(random.choices(string.digits, k=10)),
            "location": random.choice(["100 Main St", "500 Elm St", "200 Broadway"]),
            "emergency_type": random.choice(["POLICE", "MEDICAL", "FIRE"]),
            "incident_number": incident_number,  
            "priority_level": random.choice(["LOW", "MEDIUM", "HIGH", "CRITICAL"]),
            "status": random.choice(["ACTIVE", "IN_PROGRESS", "COMPLETED"])
        }, headers=headers)

        if response.status_code == 201:
            self.created_calls.append(call_sid)  # Store successful call SIDs

    @task(1)
    def log_interaction(self):
        """Only log interactions for existing calls"""
        if not self.token or not self.created_calls:
            return  

        headers = {"Authorization": f"Bearer {self.token}"}
        call_sid = random.choice(self.created_calls)  

        response = self.client.post(f"/api/calls/{call_sid}/interactions/", json={
            "speaker": "SYSTEM",
            "message": "Emergency responders are en route."
        }, headers=headers)

        if response.status_code != 201:
            print(f"Log Interaction Failed [{response.status_code}]: {response.text}")
