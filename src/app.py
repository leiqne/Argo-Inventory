import os
from flask import Flask, request, redirect, render_template
from controllers.inventory_controller import leer_inventario, agregar_envase, obtener_nuevo_id  # Importar la función obtener_nuevo_id
from datetime import datetime

app = Flask(__name__)

@app.get("/")
def index():
    envases = leer_inventario()
    return render_template('index.html', envases=envases)

@app.route('/agregar_envase', methods=['POST'])
def agregar_envase_route():
    id = request.form['id'].strip() 
    if not id:
        id = obtener_nuevo_id()  

    cliente = request.form['cliente']
    guia_remision = request.form['guia_remision'].split(',')  # Separar por comas
    tipos_envase = request.form['tipo_envase'].split(',')  # Separar por comas
    cantidades = list(map(int, request.form['cantidades'].split(',')))  # Separar por comas y convertir a enteros
    fecha = request.form['fecha'].strip() if request.form['fecha'].strip() else datetime.today().strftime('%Y-%m-%d')
    cancelado = 'cancelado' in request.form

    agregar_envase(id, cliente, guia_remision, tipos_envase, cantidades, fecha, cancelado) 
    return redirect('/')



if __name__ == '__main__':
    app.run(debug=True)
