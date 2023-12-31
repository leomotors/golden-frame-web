from flask import Flask
from flask_limiter import Limiter

from utils import get_ip

app = Flask(__name__, static_folder="../dist", static_url_path="/")

limiter = Limiter(
    get_ip,
    app=app,
    storage_uri="memory://",
    strategy="fixed-window"
)
