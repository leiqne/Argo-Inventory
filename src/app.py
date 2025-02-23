import os
import sys
from pathlib import Path
from flask import Flask
from .routes import app_router

def utility_processor():
    colors = [ "indigo", "blue", "pink", "amber", "emerald", "sky", "purple", "slate" ] * 2
    return dict(colors=colors)

def create_app() -> Flask:
    app = Flask(__name__)
    if getattr(sys,'frozen', False):
        base_dir = Path(sys.executable).parent
    else:
        base_dir = Path(os.getcwd()) 
    app.config["folder_data"] = base_dir/ "data"
    
    app.register_blueprint(app_router)

    app.context_processor(utility_processor)
    return app