import sys
import os
from src.app import create_app

app = create_app()

if getattr(sys, 'frozen', False):
    app.static_folder = os.path.join(sys._MEIPASS, 'static')
    app.template_folder = os.path.join(sys._MEIPASS, 'templates')
else:
    # Si está en el modo de desarrollo
    app.static_folder = 'static'
    app.template_folder = 'templates'

if __name__ == '__main__':
    app.run(debug=True)
