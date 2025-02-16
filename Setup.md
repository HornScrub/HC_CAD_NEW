# Django Project Setup & Database Configuration Guide

## **1. Setting Up Your Environment**

### **Activate Virtual Environment**
Before running any Django commands, ensure your virtual environment is activated:
```sh
source env/bin/activate  # On macOS/Linux
env\Scripts\activate     # On Windows (Git Bash/PowerShell)
```

## **2. Database Setup**

### **Check Available Databases**
Before connecting to PostgreSQL, ensure you have the correct databases set up:
```sh
psql -U postgres -c "\l"  # List all databases
```

### **Switch Between Production & Test Database**
To check which database is currently active in Django:
```sh
python manage.py dbshell
```
If you need to switch manually within PostgreSQL:
```sql
\c dispatch_db         -- Switch to production DB
\c test_dispatch_db    -- Switch to test DB
```

### **Create a Test Database (If Needed)**
If `test_dispatch_db` does not exist:
```sql
CREATE DATABASE test_dispatch_db;
ALTER DATABASE test_dispatch_db OWNER TO dispatch_test_user;
```

Grant permissions to the test user:
```sql
GRANT ALL PRIVILEGES ON DATABASE test_dispatch_db TO dispatch_test_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO dispatch_test_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO dispatch_test_user;
```

## **3. Running Migrations**
After setting up the database, apply migrations:
```sh
python manage.py migrate
```
If using the test database:
```sh
export USE_TEST_DB=True
python manage.py migrate
```

## **4. Running the Django Server**
To start the Django development server:
```sh
python manage.py runserver
```
Ensure your `.env` file contains the correct database credentials before launching.

## **5. Managing Users & Authentication**

### **Create a Superuser (Admin Access)**
If you haven't created an admin user yet:
```sh
python manage.py createsuperuser
```
Follow the prompts to set a username and password.

### **Generating an Access Token for API Testing (Postman, Locust, etc.)**
Authenticate to get an access token:
```sh
curl -X POST http://127.0.0.1:8000/api/token/ -H "Content-Type: application/json" -d '{"username": "test1", "password": "whateveryouwant"}'
```

This will return a token:
```json
{
    "access": "your_jwt_access_token",
    "refresh": "your_jwt_refresh_token"
}
```
Use the `access` token in requests:
```sh
curl -X GET http://127.0.0.1:8000/api/calls/INC001/ -H "Authorization: Bearer your_jwt_access_token"
```

## **6. Running Tests**
To run unit tests for models and API endpoints:
```sh
python manage.py test
```

If testing the AI Dispatcher Integration:
```sh
python manage.py test calls.test_suite.test_integration
```

## **7. Load Testing with Locust**
Ensure the server is running before executing Locust:
```sh
locust -f locustfile.py --host=http://127.0.0.1:8000
```
Access the Locust web UI at `http://localhost:8089/` to start the load test.

---

## **8. Deployment Steps (For New Environments)**
1. **Clone the Repository**
   ```sh
   git clone https://github.com/your-repo.git
   cd your-repo
   ```

2. **Create a Virtual Environment**
   ```sh
   python -m venv env
   source env/bin/activate  # (Windows: env\Scripts\activate)
   ```

3. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```

4. **Set Up Database**
   ```sh
   psql -U postgres -c "CREATE DATABASE dispatch_db;"
   psql -U postgres -c "CREATE DATABASE test_dispatch_db;"
   ```
   Grant permissions as needed (refer to step 2).

5. **Apply Migrations**
   ```sh
   python manage.py migrate
   ```

6. **Run Server**
   ```sh
   python manage.py runserver
   ```

7. **Verify Everything Works**
   - Log into Django Admin (`http://127.0.0.1:8000/admin/`)
   - Use Postman or cURL to test API authentication and responses.
   
---
### **Additional Notes**
- Use `USE_TEST_DB=True` to switch databases without modifying `settings.py`
- Ensure `.env` variables match the correct DB credentials
- If database migrations are missing, run `python manage.py makemigrations && python manage.py migrate`

