import csv
import os
from datetime import datetime
import pandas as pd
from pathlib import Path

path_data = Path(__file__).parent.parent / "data"

CSV_PATH = os.path.join(os.path.dirname(__file__), '../data/inventario.csv')

def delete_from_csv(file_path, item_id):
    """Elimina un registro de un archivo CSV basado en su ID"""
    file_path = path_data / file_path  # Convertir a ruta absoluta
    rows = []

    if not file_path.exists():
        return

    with open(file_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader)
        rows = [row for row in reader if row[0] != str(item_id)]

    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(rows)

def delete_record(client_name, item_id):
    """Eliminar un registro de ambos archivos (cliente e inventario)"""
    delete_from_csv(f"{client_name}.csv", item_id)
    delete_from_csv("inventario.csv", item_id)

def change_registro(client_name, reg_id):
    reg_id=int(reg_id)
    df = pd.read_csv(path_data / f"{client_name}.csv")
    df.loc[df["id"]==reg_id, "estado"]="cancelado"
    df.to_csv(path_data / f"{client_name}.csv", index=False)
    
    df = pd.read_csv(path_data / "inventario.csv")
    df.loc[df["id"]==reg_id, "estado"]="cancelado"
    df.to_csv(path_data / "inventario.csv", index=False)


def leer_inventario():
    """Lee todos los registros del archivo CSV y convierte listas separadas por comas en listas reales de Python."""
    inventario = []
    with open(CSV_PATH, mode='r', newline='', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file, delimiter=',')
        
        for i, row in enumerate(reader, start=1):
            
            # Saltar filas vacías
            if not any(row.values()): 
                continue
            
            try:
                row['id'] = int(row.get('id', 0))
            except ValueError:
                row['id'] = 0

            row['fecha'] = row.get('fecha')
            
            # Convertir cadenas separadas por comas en listas
            row['guias_remision'] = [item.strip() for item in row.get('guias_remision', '').split(',') if item.strip()]
            row['tipos_envase'] = [item.strip() for item in row.get('tipos_envase', '').split(',') if item.strip()]
            row['cantidades'] = [item.strip() for item in row.get('cantidades', '').split(',') if item.strip()]
            
            # Dejar el estado tal cual (en minúsculas para uniformidad)
            row['estado'] = row.get('estado', '').strip().lower()
            
            # Agregar la fila procesada al inventario
            inventario.append(row)
    return inventario

def get_csv_cliente(client_name):
    """Lee todos los registros del archivo CSV y convierte listas separadas por comas en listas reales"""
    inventario = []
    with open(path_data / f"{client_name}.csv", mode='r', newline='', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file, delimiter=',')
        
        for i, row in enumerate(reader, start=1):
            # Saltar filas vacías
            if not any(row.values()): 
                continue
            
            # Conversión de ID (maneja errores si no es entero)
            try:
                row['id'] = int(row.get('id', 0))
            except ValueError:
                row['id'] = 0
            
            # Conversión de fecha (si está vacía, usa la fecha de hoy)
            row['fecha'] = row.get('fecha') if row.get('fecha') else datetime.today().strftime('%Y-%m-%d')
            
            # Conversión de listas separadas por comas
            row['guias_remision'] = [item.strip() for item in row.get('guias_remision', '').split(',') if item.strip()]
            row['tipos_envase'] = [item.strip() for item in row.get('tipos_envase', '').split(',') if item.strip()]
            row['cantidades'] = [item.strip() for item in row.get('cantidades', '').split(',') if item.strip()]
            
            # Conversión de estado a booleano
            row['estado'] = row.get('estado', 'False').strip()

            
            inventario.append(row)
    
    return inventario

def add_cliente(client_name):
    df = pd.DataFrame(columns=['id','cliente','fecha','guias_remision','tipos_envase','cantidades','estado'])
    df.to_csv(path_data / f"{client_name}.csv", index=False)

def envases_pendientes(client_name):
    contador_pendientes = 0
    
    with open(path_data / f"{client_name}.csv", mode='r', newline='', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file, delimiter=',')
        
        for fila in reader:
            if fila.get('estado') == 'pendiente':
                contador_pendientes += 1   
    return contador_pendientes

def listar_clientes():
    return [file.stem for file in path_data.glob("*.csv") if file.stem != "inventario"]

def agregar_envase(nuevo_id, cliente, guias_remision, tipos_envase, cantidades, fecha_hoy=None, estado='pendiente'):
    """
    Agrega un nuevo envase con múltiples guías de remisión, tipos de envases y cantidades.
    Retorna un error si el ID ya existe en el archivo del cliente.
    """
    if not fecha_hoy:
        fecha_hoy = datetime.today().strftime('%Y-%m-%d')
        
    # Crear la ruta específica para el cliente
    client_csv_path = path_data / f"{cliente}.csv"
    
    # Verificar si el archivo del cliente existe y si el ID ya está en uso
    if client_csv_path.exists():
        with open(client_csv_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if int(row.get('id', 0)) == nuevo_id:
                    print("hola que tal")
                    print(nuevo_id)
                    raise ValueError(f"El ID {nuevo_id} ya existe en el archivo de {cliente}.csv.")

    # Convertir las cantidades a enteros y asegurarse de que las listas se guarden como cadenas separadas por comas
    cantidades = [int(float(c)) for c in cantidades]
    guias_remision_str = ','.join(guias_remision)
    tipos_envase_str = ','.join(tipos_envase)
    cantidades_str = ','.join(map(str, cantidades))

    registro = {
        'id': nuevo_id,
        'cliente': cliente,
        'fecha': fecha_hoy,
        'guias_remision': guias_remision_str,
        'tipos_envase': tipos_envase_str,
        'cantidades': cantidades_str,
        'estado': estado
    }
    
    # Agregar el registro al archivo específico del cliente
    with open(client_csv_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['id', 'cliente', 'fecha', 'guias_remision', 'tipos_envase', 'cantidades', 'estado'])
        
        if file.tell() == 0:
            writer.writeheader()
        
        writer.writerow(registro)
    
    # Agregar el mismo registro al archivo general 'inventario.csv'
    with open(CSV_PATH, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['id', 'cliente', 'fecha', 'guias_remision', 'tipos_envase', 'cantidades', 'estado'])
        
        if file.tell() == 0:
            writer.writeheader()
        
        writer.writerow(registro)


def obtener_nuevo_id():
    """Obtiene un nuevo ID incremental para el próximo registro."""
    inventario = leer_inventario()
    ids = [row['id'] for row in inventario if isinstance(row['id'], int)]
    return max(ids, default=0) + 1

def buscar_envase(id_envase):
    """Busca un envase por ID."""
    inventario = leer_inventario()
    for row in inventario:
        if int(row['id']) == id_envase:
            return row
    return None

def buscar_envase_por_guia(guia_remision):
    """Busca un envase por la Guía de Remisión."""
    inventario = leer_inventario()
    for row in inventario:
        if row['guia_remision'] == guia_remision:
            return row
    return None