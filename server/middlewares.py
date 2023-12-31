from datetime import datetime

from flask import request, Response

from app import app
from env import PASSWORD, password_is_ok
from utils import get_ip


@app.after_request
def log_response(response: Response):
    if request.path == "/health" and password_is_ok and request.headers.get("Authorization") == PASSWORD:
        return response

    now = datetime.now()
    print(f"[{now.strftime('%d/%m/%Y %H:%M:%S')}] {get_ip()} -> {request.method} {request.path} {response.status_code}")
    return response
