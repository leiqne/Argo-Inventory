import os
from pathlib import Path
from flask import Flask
from .routes import app_router

def create_app() -> Flask:
    app = Flask(__name__)
    app.config["folder_data"] = Path(__file__).parent.parent / "data"
    
    # register Blueprints (routes)
    app.register_blueprint(app_router)

    return app
