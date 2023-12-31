import os

PASSWORD = os.getenv("PASSWORD")

if PASSWORD is None or len(PASSWORD) < 6:
    raise Exception("PASSWORD environment variable is not set or too weak!")
