from flask import Blueprint, request, render_template, jsonify
from ..controllers.inventory_controller import (
    leer_inventario,
    agregar_envase,
    get_csv_cliente,
    add_cliente,
    listar_clientes
)

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


@app_router.delete('/api/pendientes/<string:client_name>')
def delete_pendiente(client_name:str):
    try:
        data = request.get_json()
        id = data.get('id')
        envases = get_csv_cliente(client_name)
        envases = list(filter(lambda x: x["id"] != id, envases))
        # guardar de nuevo el csv
        print(envases)
        return jsonify({'message': 'Registro eliminado exitosamente'}), 200
    except Exception as e:
        print(f"Error al eliminar registro: {e}")
        return jsonify({'error': 'Hubo un error al eliminar el registro'}), 500

@app_router.post('/add-devolucion')
def agregar_devolucion_route():
    try:
        # Obtén los datos del registro de devolución desde la solicitud
        data = request.get_json()
        print(f"Datos recibidos: {data}")

        # Extraer datos de la solicitud
        cliente = data.get('cliente')
        nuevo_id = data.get('id')
        fecha = data.get('fecha')
        guias_remision = data.get('guias_remision')
        tipos_envase = data.get('tipos_envase')
        cantidades = data.get('cantidades')
        estado = data.get('estado')  # Valor predeterminado 'Pendiente'

        # Validar los campos obligatorios
        if not cliente or not nuevo_id or not fecha or not guias_remision or not tipos_envase or not cantidades:
            return jsonify({'error': 'Todos los campos son obligatorios'}), 400

        # Convertir listas en caso de que sean cadenas separadas por comas
        if isinstance(guias_remision, str):
            guias_remision = guias_remision.split(',')
        if isinstance(tipos_envase, str):
            tipos_envase = tipos_envase.split(',')
        if isinstance(cantidades, str):
            cantidades = list(map(float, cantidades.split(',')))

        # Verificar que la longitud de tipos_envase y cantidades coincidan
        if len(tipos_envase) != len(cantidades):
            return jsonify({'error': 'La cantidad de tipos de envase no coincide con las cantidades proporcionadas'}), 400

        # Agregar registro al CSV
        agregar_envase(
            nuevo_id=nuevo_id,
            cliente=cliente,
            guias_remision=guias_remision,
            tipos_envase=tipos_envase,
            cantidades=cantidades,
            fecha_hoy=fecha,
            estado=estado
        )

        return jsonify({'message': 'Registro de devolución agregado exitosamente'}), 200

    except Exception as e:
        print(f"Error al agregar devolución: {e}")
        return jsonify({'error': 'Hubo un error al guardar el registro de devolución'}), 500


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
