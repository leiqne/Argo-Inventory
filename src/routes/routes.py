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


@app_router.post('/add-devolucion')
def agregar_devolucion_route():
    try:
        # Obtén los datos del registro de devolución desde la solicitud
        data = request.get_json()
        print(f"Datos recibidos: {data}")
        cliente = data.get('cliente')
        guia_remision = data.get('guia_remision')
        tipo_envase = data.get('tipo_envase')
        cantidad = data.get('cantidad')
        fecha = data.get('fecha')
        
        if not cliente or not guia_remision or not tipo_envase or not cantidad:
            return jsonify({'error': 'Todos los campos son obligatorios'}), 400

        # Procesar y agregar lógica de negocio aquí
        print(f"Datos recibidos: {data}")
        
        return jsonify({'message': 'Registro de devolución agregado exitosamente'}), 200
    except Exception as e:
        print(f"Error al agregar devolución: {e}")
        return jsonify({'error': 'Error al procesar el registro de devolución'}), 500

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