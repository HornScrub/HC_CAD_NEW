import os
from functools import wraps

def require_test_db(func):
    """Decorator to prevent running tests unless the test database is in use."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if os.getenv("USE_TEST_DB", "False") != "True":
            raise RuntimeError("Switch to the test database before running this test! Set USE_TEST_DB=True.")
        return func(*args, **kwargs)
    return wrapper
