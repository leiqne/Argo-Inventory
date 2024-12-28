from flask import Blueprint, request, render_template, redirect, jsonify
from ..controllers.inventory_controller import leer_inventario, agregar_envase, obtener_nuevo_id, get_csv_cliente, add_cliente, listar_clientes
from datetime import datetime

app_router = Blueprint("app_router", __file__)

@app_router.get("/")
def index():
    clientes = listar_clientes()
    print (f"clientes", clientes)
    return render_template('index.html', clientes=clientes, zip=zip)

@app_router.get("/inventario")
def inventario():
    envases = leer_inventario()
    return render_template('inventario.html', envases=envases, zip=zip, path=[{'name': 'inventario', 'url':'#'}])

@app_router.get("/pendientes/<string:client_name>")
def get_peendiente_by_client(client_name:str):
    data = filter(lambda x: x["estado"] == "pendiente", get_csv_cliente(client_name))
    return render_template('sumary_pend.html', client_name=client_name, paths=[{'name': 'pendientes', 'url':'#'}, {'name': client_name, 'url':f'#{client_name}'}], envases=data, zip=zip)


@app_router.route('/agregar_envase', methods=['POST'])
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

@app_router.post('/add-cliente')
def agregar_cliente_route():
    try:
        # Obtén los datos del cliente desde la solicitud
        data = request.get_json()
        client_name = data.get('client_name')

        if not client_name:
            return jsonify({'error': 'El nombre del cliente es obligatorio'}), 400

        # Llama a la función add_cliente
        add_cliente(client_name)
        return jsonify({'message': 'Cliente agregado exitosamente'}), 200
    except Exception as e:
        print(f"Error al agregar cliente: {e}")
        return jsonify({'error': 'Error al agregar el cliente'}), 500