# Test Suite - CAD_BACKEND

This directory contains all testing scripts for the CAD_BACKEND system, including Django unit tests and Locust load tests.

---

## Running Django Unit Tests

Django's built-in test framework is used for unit and integration testing.

### 1. Ensure the Test Database is Active
Before running Django tests, ensure the test database is being used. You can set this by:

```sh
export USE_TEST_DB=True  # Linux/macOS
set USE_TEST_DB=True     # Windows (cmd)
$env:USE_TEST_DB="True"  # Windows (PowerShell)
```

### 2. Run Tests
To execute all Django tests, run:

```sh
python manage.py test
```

To run tests from a specific module:

```sh
python manage.py test calls.test_suite.test_integration
```

To see detailed test output:

```sh
python manage.py test --verbosity=2
```

---

## Running Load Tests with Locust

Locust is used for simulating realistic user behavior on the API.

### 1. Ensure the Test Database is Active
WARNING: Load tests generate real database entries. Ensure the test database is in use before running.

```sh
export USE_TEST_DB=True  # Linux/macOS
set USE_TEST_DB=True     # Windows (cmd)
$env:USE_TEST_DB="True"  # Windows (PowerShell)
```

### 2. Start the Locust Load Test
Navigate to the test_suite directory:

```sh
cd test_suite
```

Run the Locust web UI:

```sh
locust -f locustfile_clean.py --host=http://127.0.0.1:8000
```

### 3. Open Locust UI
Once Locust is running, open your browser and go to:

```
http://localhost:8089
```

Enter:
- Number of users (simulated clients)
- Spawn rate (users per second)

Click "Start Swarming" to begin load testing.

### 4. Run Locust in CLI Mode (Optional)
To run Locust without the UI, use:

```sh
export USE_TEST_DB=True
locust -f locustfile_clean.py --headless --users 100 --spawn-rate 10 --host=http://127.0.0.1:8000
```

This runs 100 concurrent users, spawning 10 new users per second.

---

## Troubleshooting

### Check the Active Database
To confirm which database is in use:

```sh
python manage.py dbshell
```

Then run:

```sql
SELECT current_database();
```

If it's not the test database, restart the process after setting USE_TEST_DB=True.

### Missing Locust?
If Locust isn't installed, install it with:

```sh
pip install locust
```

### Locust Tests Not Running?
Ensure:
- The Django server is running: `python manage.py runserver`
- You have an active access token (Locust fetches it on startup)
- The test database is active (`USE_TEST_DB=True`)

### To Clear Test DB
- python manage.py sqlflush --database=persistent_test
OR
psql -U test_dispatch_user -d test_dispatch_db
TRUNCATE TABLE django_migrations, calls_call, calls_callinteraction RESTART IDENTITY CASCADE;


---

## Summary

| Test Type                     | Command |
|--------------------------------|-------------------------------------|
| Run all Django tests          | `python manage.py test` |
| Run specific test file        | `python manage.py test calls.test_suite.test_integration` |
| Run Django tests (verbose)    | `python manage.py test --verbosity=2` |
| Start Locust Web UI           | `locust -f locustfile_clean.py --host=http://127.0.0.1:8000` |
| Run Locust headless (CLI)     | `locust -f locustfile_clean.py --headless --users 100 --spawn-rate 10 --host=http://127.0.0.1:8000` |

