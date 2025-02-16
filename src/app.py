import os
from pathlib import Path
from flask import Flask
from .routes import app_router

def utility_processor():
  colors = [ "indigo", "blue", "pink", "amber", "emerald", "sky", "purple", "slate" ] * 2
  
  return dict(colors=colors)

def create_app() -> Flask:
    app = Flask(__name__)
    app.config["folder_data"] = Path(__file__).parent.parent / "data"
    
    # register Blueprints (routes)
    app.register_blueprint(app_router)

    # context processors
    app.context_processor(utility_processor)
    return app
