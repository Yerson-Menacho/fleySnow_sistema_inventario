from app.models import get_db_connection
import mysql.connector

# ✅ Insertar rol
def insertar_rol(nombre_rol, descripcion):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.callproc("sp_insertar_rol", (nombre_rol, descripcion))
        conn.commit()
    except mysql.connector.Error as e:
        conn.rollback()
        raise ValueError(f"Error al insertar rol: {e}")
    finally:
        cursor.close()
        conn.close()

# ✅ Listar roles
def listar_roles():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.callproc("sp_listar_roles")
    roles = []
    for res in cursor.stored_results():
        roles = res.fetchall()
    cursor.close()
    conn.close()
    return roles
