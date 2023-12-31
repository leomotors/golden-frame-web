import os

PASSWORD = os.getenv("PASSWORD")
password_is_ok = True

if PASSWORD is None or len(PASSWORD) < 6:
    password_is_ok = False
    print("WARNING: PASSWORD environment variable is not set or too weak! All health check will be logged")
