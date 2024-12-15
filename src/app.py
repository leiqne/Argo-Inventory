import os
from flask import Flask, request, redirect, render_template
from controllers.inventory_controller import leer_inventario, agregar_envase
from datetime import datetime
app = Flask(__name__)


@app.get("/")
def index():
    envases = leer_inventario()
    return render_template('index.html', envases=envases)

@app.route('/agregar_envase', methods=['POST'])
def agregar_envase_route():
    cliente = request.form['cliente']
    tipo_envase = request.form['tipo_envase']
    fecha = request.form['fecha'] if 'fecha' in request.form else datetime.today().strftime('%Y-%m-%d')  
    cancelado = 'cancelado' in request.form

    agregar_envase(cliente, tipo_envase, fecha, cancelado) 
    return redirect('/')


if __name__ == '__main__':
    
    app.run(debug=True)
