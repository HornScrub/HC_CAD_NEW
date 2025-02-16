import os
from locust import HttpUser, task, between
import random
import string

class DispatcherLoadTest(HttpUser):
    wait_time = between(1, 3)
    host = "http://127.0.0.1:8000"
    token = None  
    created_calls = []  # Store created calls to avoid unnecessary 404 errors

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
        """Create valid calls and store them"""
        if not self.token:
            return

        headers = {"Authorization": f"Bearer {self.token}"}
        call_sid = self.generate_call_sid()
        incident_number = self.generate_incident_number()

        response = self.client.post("/api/calls/", json={
            "call_sid": call_sid,
            "caller_number": "+1" + "".join(random.choices(string.digits, k=10)),
            "location": random.choice(["100 Main St", "500 Elm St", "200 Broadway"]),
            "emergency_type": random.choice(["POLICE", "MEDICAL", "FIRE"]),
            "incident_number": incident_number,  # Now independent from call_sid
            "priority_level": random.choice(["LOW", "MEDIUM", "HIGH", "CRITICAL"]),
            "status": random.choice(["ACTIVE", "IN_PROGRESS", "COMPLETED"])
        }, headers=headers)

        if response.status_code == 201:
            self.created_calls.append(call_sid)  

    @task(1)
    def log_interaction(self):
        """Log interactions, with some invalid requests for realism"""
        if not self.token:
            return  

        headers = {"Authorization": f"Bearer {self.token}"}
        
        if random.random() < 0.2:  # 20% chance of using a fake call_sid
            call_sid = self.generate_call_sid()  
        else:
            if not self.created_calls:
                return  
            call_sid = random.choice(self.created_calls)  

        response = self.client.post(f"/api/calls/{call_sid}/interactions/", json={
            "speaker": "SYSTEM",
            "message": "Emergency responders are en route."
        }, headers=headers)

        if response.status_code != 201:
            print(f"Log Interaction Failed [{response.status_code}]: {response.text}")

    @task(1)
    def update_call_status(self):
        """Update calls, with occasional invalid requests"""
        if not self.token:
            return  

        headers = {"Authorization": f"Bearer {self.token}"}

        if random.random() < 0.3:  # 30% chance of using a fake call_sid
            call_sid = self.generate_call_sid()  
        else:
            if not self.created_calls:
                return  
            call_sid = random.choice(self.created_calls)  

        response = self.client.put(f"/api/calls/{call_sid}/", json={
            "status": random.choice(["ACTIVE", "CANCELLED", "COMPLETED"])
        }, headers=headers)

        if response.status_code != 200:
            print(f"Update Call Failed [{response.status_code}]: {response.text}")
