import csv
import os
from datetime import datetime
import pandas as pd
from pathlib import Path

path_data = Path(__file__).parent.parent / "data"

CSV_PATH = os.path.join(os.path.dirname(__file__), '../data/inventario.csv')


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
            
            row['guias_remision'] = [item.strip() for item in row.get('guias_remision', '').split(',') if item.strip()]
            row['tipos_envase'] = [item.strip() for item in row.get('tipos_envase', '').split(',') if item.strip()]
            row['cantidades'] = [item.strip() for item in row.get('cantidades', '').split(',') if item.strip()]
            
            row['estado'] = row.get('estado', 'False').strip().lower() == 'true'
            
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



def listar_clientes():
    return [file.stem for file in path_data.glob("*.csv") if file.stem != "inventario"]

def agregar_envase(nuevo_id, cliente, guias_remision, tipos_envase, cantidades, fecha_hoy=None, estado='pendiente'):
    """
    Agrega un nuevo envase con múltiples guías de remisión, tipos de envases y cantidades.
    No se realiza ninguna verificación para comprobar si el ID ya existe.
    """
    if not fecha_hoy:
        fecha_hoy = datetime.today().strftime('%Y-%m-%d')
        
    cantidades = [int(float(c)) for c in cantidades]
    # Asegurarse de que las listas se guarden como cadenas separadas por comas
    guias_remision_str = ','.join(guias_remision)
    tipos_envase_str = ','.join(tipos_envase)
    cantidades_str = ','.join(map(str, cantidades))

    with open(CSV_PATH, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['id', 'cliente', 'fecha', 'guias_remision', 'tipos_envase', 'cantidades', 'estado'])
        
        if file.tell() == 0:  # Escribir encabezado solo si el archivo está vacío
            writer.writeheader()
        
        writer.writerow({
            'id': nuevo_id,
            'cliente': cliente,
            'fecha': fecha_hoy,
            'guias_remision': guias_remision_str,
            'tipos_envase': tipos_envase_str,
            'cantidades': cantidades_str,
            'estado': estado
        })
    
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

def eliminar_envase(id_envase):
    """Elimina un envase por su ID."""
    inventario = leer_inventario()
    nuevos_datos = [row for row in inventario if row['id'] != id_envase]
    with open(CSV_PATH, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['id', 'guia_remision', 'cliente', 'fecha', 'tipo_envase', 'estado'])
        writer.writeheader()
        writer.writerows(nuevos_datos)

