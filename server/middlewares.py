from datetime import datetime

from flask import request, Response

from app import app
from env import PASSWORD


def getIP():
    return request.headers.get("cf-connecting-ip") or request.headers.get(
        "x-real-ip") or request.remote_addr


@app.after_request
def log_response(response: Response):
    if request.path == "/health" and request.headers.get("Authorization") == PASSWORD:
        return response

    now = datetime.now()
    print(f"[{now.strftime('%d/%m/%Y %H:%M:%S')}] {getIP()} -> {request.method} {request.path} {response.status_code}")
    return response
