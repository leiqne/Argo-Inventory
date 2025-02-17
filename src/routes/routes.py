from flask import Blueprint, request, render_template, jsonify
from ..controllers.inventory_controller import (
    leer_inventario,
    agregar_envase,
    add_cliente,
    listar_clientes,
    envases_pendientes,
    change_registro,
    delete_record,
    obtener_nuevo_id,
    id_exists
)
from ..helpers import csv_for_table
import pandas as pd
from datetime import datetime

app_router = Blueprint("app_router", __file__)
from datetime import datetime

@app_router.get("/")
def index():
    clientes = listar_clientes()
    clientes_con_pendientes = []
    new_id = obtener_nuevo_id()
    fecha = datetime.now().strftime('%Y-%m-%d')
    
    for cliente in clientes:
        pendientes = envases_pendientes(cliente)
        clientes_con_pendientes.append({"nombre": cliente, "pendientes": pendientes})
    
    return render_template('index.html', clientes=clientes_con_pendientes, new_id=new_id, fecha_now=fecha)


@app_router.delete('/api/inventario/<int:item_id>')
def delete_inventario(item_id):
    """Elimina un registro del inventario y del archivo del cliente"""
    try:
        # Obtener los datos actuales del inventario
        envases = leer_inventario()
        cliente_nombre = None

        # Buscar el nombre del cliente asociado al ID
        for envase in envases:
            if envase['id'] == item_id:
                cliente_nombre = envase['cliente']
                break

        if not cliente_nombre:
            return jsonify({'error': 'No se encontró el cliente asociado'}), 404

        # Eliminar el registro de ambos archivos
        delete_record(cliente_nombre, item_id)

        return jsonify({'message': 'Registro eliminado exitosamente'}), 200
    except Exception as e:
        print(f"Error al eliminar el registro: {e}")
        return jsonify({'error': 'No se pudo eliminar el registro'}), 500

@app_router.get("/inventario")
def inventario():
    # Obtener todos los envases
    envases = leer_inventario()

    # Obtener los parámetros de filtro y orden
    filter_type = request.args.get('filter_type', default=None, type=str)
    filter_value = request.args.get('filter_value', default=None, type=str)
    sort_by = request.args.get('sort_by', default='id', type=str) 

    # Aplicar filtro si se proporciona
    if filter_type and filter_value:
        if filter_type == 'id':
            envases = [envase for envase in envases if str(envase['id']) == filter_value]
        elif filter_type == 'year':
            try:
                envases = [envase for envase in envases if datetime.strptime(envase['fecha'], '%Y-%m-%d').year == int(filter_value)]
            except ValueError:
                pass

    # Ordenar los envases
    if sort_by == 'id':
    # Ordenar por id
        envases_ordenados = sorted(envases, key=lambda x: (x['estado'] != 'pendiente', x['id'] if x['estado'] == 'pendiente' else -x['id']))
    else:
    # Ordenar por fecha
        envases_ordenados = sorted(envases, key=lambda x: (
            x['estado'] != 'pendiente',  # Los pendientes primero (False < True)
            datetime.strptime(x['fecha'], '%Y-%m-%d') if x['estado'] == 'pendiente' else datetime.max - datetime.strptime(x['fecha'], '%Y-%m-%d'),  # Ascendente para pendientes, descendente para no pendientes
            x['id'] if x['estado'] == 'pendiente' else -x['id']  # Ascendente por id para pendientes, descendente para no pendientes
        ))
    # Paginación
    page = request.args.get('page', 1, type=int)
    per_page = 20
    start = (page - 1) * per_page
    end = start + per_page
    paginated_envases = envases_ordenados[start:end]
    total_pages = (len(envases_ordenados) + per_page - 1) // per_page
    return render_template(
        'inventario.html',
        envases=paginated_envases,
        page=page,
        total_pages=total_pages,
        zip=zip,
        path=[{'name': 'inventario', 'url': '#'}],
        filter_type=filter_type,
        filter_value=filter_value,
        sort_by=sort_by,
        client_name=None
    )

@app_router.get("/pendientes/<string:client_name>")
def get_peendiente_by_client(client_name:str):
    df = csv_for_table(path=f"src/data/{client_name}.csv", to_dict=False, aggf={'estado': 'first'})
    df = df[df['estado'] == 'pendiente']
    return render_template('sumary_pend.html', client_name=client_name, envases=df, zip=zip)


@app_router.get("/summary/<string:client_name>")
def summary(client_name: str):
    df = csv_for_table(path=f"src/data/{client_name}.csv", to_dict=False, aggf={'estado': 'first'})
    
    # Ordenar por estado según prioridad
    orden = ['pendiente', 'cancelado', 'anulado']
    df['estado'] = pd.Categorical(df['estado'], categories=orden, ordered=True)
    df_ordenado = df.sort_values(by='estado')

    # Convertir el DataFrame en una lista de diccionarios
    envases = df_ordenado.to_dict(orient="records")

    # Paginación
    page = request.args.get('page', 1, type=int)
    per_page = 20
    start = (page - 1) * per_page
    end = start + per_page
    paginated_envases = envases[start:end]
    total_pages = (len(envases) + per_page - 1) // per_page

    return render_template(
        'inventario.html',  # Reutilizando la plantilla de inventario
        envases=paginated_envases,
        page=page,
        total_pages=total_pages,
        zip=zip,
        path=[{'name': 'summary', 'url': '#'}, {'name': client_name, 'url': f'#{client_name}'}],
        filter_type=None,
        filter_value=None,
        sort_by='estado',
        client_name=client_name  # Pasamos el nombre del cliente a la plantilla
    )


@app_router.delete('/api/pendientes/<string:client_name>')
def delete_pendiente(client_name:str):
    try:
        data = request.get_json()
        id = data.get('id')
        change_registro(client_name, id)
        return jsonify({'message': 'Registro eliminado exitosamente'}), 200
    except Exception as e:
        print(f"Error al eliminar registro: {e}")
        return jsonify({'error': 'Hubo un error al eliminar el registro'}), 500

@app_router.post('/add-devolucion')
def agregar_devolucion_route():
    try:
        # Obtén los datos del registro de devolución desde la solicitud
        data = request.get_json()
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
        if id_exists(nuevo_id):
            return jsonify({'error': 'El ID ya existe'}), 400
        if isinstance(guias_remision, str):
            guias_remision = guias_remision.split(',')
        if isinstance(tipos_envase, str):
            tipos_envase = tipos_envase.split(',')
        if isinstance(cantidades, str):
            cantidades = list(map(float, cantidades.split(',')))
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
