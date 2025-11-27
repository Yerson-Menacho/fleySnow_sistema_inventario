from collections import defaultdict
from app.models import get_db_connection

# ✅ Listar todas las acciones (agrupadas por módulo en la vista)
def listar_acciones():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.callproc("sp_listar_acciones")

    acciones = []
    for result in cursor.stored_results():
        acciones = result.fetchall()

    cursor.close()
    conn.close()

    # Agrupar acciones por módulo
    agrupadas = defaultdict(list)
    for acc in acciones:
        agrupadas[acc["modulo"]].append(acc)

    return agrupadas 

# ✅ Guardar permisos de un usuario (ahora usando códigos)
def guardar_permisos_usuario(id_usuario, seleccionados):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Manejar caso sin permisos seleccionados
        codigos_str = ",".join(seleccionados) if seleccionados else None
        cursor.callproc("sp_guardar_permisos_usuario", [id_usuario, codigos_str])
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise ValueError(f"Error guardando permisos: {e}")
    finally:
        cursor.close()
        conn.close()

# ✅ Obtener permisos actuales de un usuario (incluye código)
def obtener_permisos_usuario(id_usuario):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.callproc("sp_obtener_permisos_usuario", [id_usuario])
    permisos = []
    for result in cursor.stored_results():
        permisos = result.fetchall()
    cursor.close()
    conn.close()
    return permisos
