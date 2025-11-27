from app.models import get_db_connection
import mysql.connector
from werkzeug.security import generate_password_hash

# ✅ Insertar usuario
def insertar_usuario(datos):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        hashed_password = generate_password_hash(datos['contrasena'])
        cursor.callproc("sp_insertar_usuario", (
            datos['nombre_completo'],
            datos['dni'],
            hashed_password,
            datos['email'],
            datos['telefono'],
            datos['id_rol']
        ))
        conn.commit()
    except mysql.connector.Error as e:
        conn.rollback()
        raise ValueError(f"Error al insertar usuario: {e}")
    finally:
        cursor.close()
        conn.close()

# ✅ Listar usuarios
def listar_usuarios():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Llamar al SP pasando los 5 parámetros requeridos (como None si no hay filtros)
    cursor.callproc("sp_listar_usuarios", [None, None, None, None, None])

    usuarios = []
    for res in cursor.stored_results():
        usuarios = res.fetchall()

    cursor.close()
    conn.close()
    return usuarios


# ✅ Obtener usuario por ID
def obtener_usuario(id_usuario):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.callproc("sp_obtener_usuario", (id_usuario,))
    usuario = None
    for res in cursor.stored_results():
        usuario = res.fetchone()
    cursor.close()
    conn.close()
    return usuario

# ✅ Actualizar usuario
def actualizar_usuario(datos):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.callproc("sp_actualizar_usuario", (
            datos['id_usuario'],
            datos['nombre_completo'],
            datos['dni'],
            datos['email'],
            datos['telefono'],
            datos['id_rol'],
            datos['estado']
        ))
        conn.commit()
    except mysql.connector.Error as e:
        conn.rollback()
        raise ValueError(f"Error al actualizar usuario: {e}")
    finally:
        cursor.close()
        conn.close()

# ✅ Cambiar contraseña
def cambiar_contrasena(id_usuario, contrasena):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.callproc("sp_cambiar_contrasena", (id_usuario, contrasena))
        conn.commit()
    except mysql.connector.Error as e:
        conn.rollback()
        raise ValueError(f"Error al cambiar contraseña: {e}")
    finally:
        cursor.close()
        conn.close()

# ✅ Login usuario
def login_usuario(dni, contrasena):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.callproc("sp_login_usuario", (dni, contrasena))
        usuario = None
        for res in cursor.stored_results():
            usuario = res.fetchone()
        return usuario
    except mysql.connector.Error as e:
        raise ValueError(f"Error en login: {e}")
    finally:
        cursor.close()
        conn.close()

# ✅ Obtener usuario por DNI
def obtener_usuario_por_dni(dni):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE dni = %s", (dni,))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()
    return usuario

# ✅ Obtener usuario por ID
def obtener_usuario_por_id(id_usuario):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (id_usuario,))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()
    return usuario
