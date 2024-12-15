import csv
import os
from datetime import datetime

CSV_PATH = os.path.join(os.path.dirname(__file__), '../data/inventario.csv')

def leer_inventario():
    """Lee todos los registros del archivo CSV y depura los valores de 'id'."""
    inventario = []
    with open(CSV_PATH, mode='r', newline='', encoding='utf-8-sig') as file:  # Usar utf-8-sig para eliminar BOM
        reader = csv.DictReader(file, delimiter=',')
        for row in reader:
            if not any(row.values()):  # Ignoramos filas completamente vacías
                continue
            try:
                row['fecha'] = row.get('fecha', datetime.today().strftime('%Y-%m-%d'))  # Usar la fecha actual si no tiene valor
                row['id'] = int(row.get('id', 0))  # Convertir 'id' a entero
            except ValueError:
                row['fecha'] = datetime.today().strftime('%Y-%m-%d')  # Usar la fecha actual si no se puede convertir
                row['id'] = 0  # Usar 0 si no se puede convertir
            row['cancelado'] = row.get('cancelado', 'False').strip().lower() == 'true'
            inventario.append(row)
    return inventario


def agregar_envase(cliente, tipo_envase, fecha_hoy=None, cancelado=False):
    """Agrega un nuevo envase al archivo CSV con la fecha de hoy si no se proporciona fecha."""
    if fecha_hoy is None or fecha_hoy == '':  # Si fecha_hoy está vacía o no se pasa
        fecha_hoy = datetime.today().strftime('%Y-%m-%d')  # Usar la fecha actual

    print(f"Fecha antes de escribir: {fecha_hoy}")  # Depuración: Verifica el valor de la fecha

    nuevo_id = obtener_nuevo_id()

    # Escribe la fila con la fecha correcta
    with open(CSV_PATH, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([nuevo_id, cliente, tipo_envase, fecha_hoy, 'True' if cancelado else 'False'])

    # Depuración: Verifica que la fila escrita tenga la fecha
    print(f"Fila agregada: {nuevo_id}, {cliente}, {tipo_envase}, {fecha_hoy}, {'True' if cancelado else 'False'}")





def obtener_nuevo_id():
    """Obtiene un nuevo ID incremental para el próximo registro."""
    inventario = leer_inventario()
    ids = [row.get('id', 0) for row in inventario]
    return max(ids, default=0) + 1


def buscar_envase(id_envase):
    """Busca un envase por ID."""
    inventario = leer_inventario()
    for row in inventario:
        if int(row['id']) == id_envase:
            return row
    return None


def eliminar_envase(id_envase):
    """Elimina un envase por su ID."""
    inventario = leer_inventario()
    nuevos_datos = [row for row in inventario if int(row['id']) != id_envase]
    with open(CSV_PATH, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['id', 'cliente', 'tipo_envase', 'fecha', 'cancelado'])
        writer.writeheader()
        writer.writerows(nuevos_datos)


elm=eliminar_envase(1057
            )
