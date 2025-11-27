import mysql.connector
from app.models import get_db_connection

# ==============================
# 📌 Listar agricultores activos
# ==============================
def listar_agricultores(codigo=None, nombre=None, dni=None, estado=None):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.callproc("sp_listar_agricultores", [codigo, nombre, dni, estado])

    resultado = []
    for res in cursor.stored_results():
        resultado = res.fetchall()

    cursor.close()
    conn.close()
    return resultado


# ==============================
# 📌 Obtener un agricultor
# ==============================
def obtener_agricultor(id_agricultor):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.callproc("sp_obtener_agricultor", (id_agricultor,))
    resultado = None
    for res in cursor.stored_results():
        resultado = res.fetchone()
    cursor.close()
    conn.close()
    return resultado

# ==============================
# 📌 Agregar agricultor
# ==============================
def agregar_agricultor(datos):
    # Validaciones
    if len(datos['codigo_agricultor']) > 5:
        raise ValueError("El código no puede tener más de 5 caracteres")
    if len(datos['dni']) != 8:
        raise ValueError("El DNI debe tener exactamente 8 caracteres")
    if datos.get('telefono') and len(datos['telefono']) != 9:
        raise ValueError("El teléfono debe tener exactamente 9 caracteres")

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.callproc("sp_insertar_agricultor", (
            datos['codigo_agricultor'],
            datos['dni'],
            datos['nombres'],
            datos['apellidos'],
            datos['telefono'],
            datos['direccion'],
            datos['correo'],
            datos['zona'],
            datos['cultivo_principal']
        ))
        conn.commit()
    except mysql.connector.IntegrityError as e:
        if "Duplicate entry" in str(e):
            raise ValueError("El código o DNI del agricultor ya existe.")
        else:
            raise
    finally:
        cursor.close()
        conn.close()

# ==============================
# 📌 Actualizar agricultor
# ==============================
def actualizar_agricultor(datos):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.callproc("sp_actualizar_agricultor", (
            datos['id_agricultor'],
            datos['codigo_agricultor'],
            datos['dni'],
            datos['nombres'],
            datos['apellidos'],
            datos['telefono'],
            datos['direccion'],
            datos['correo'],
            datos['zona'],
            datos['cultivo_principal'],
            datos['estado']  # 1 = Activo, 0 = Inactivo
        ))
        conn.commit()
    finally:
        cursor.close()
        conn.close()

# ==============================
# 📌 Desactivar agricultor (borrado lógico)
# ==============================
def desactivar_agricultor(id_agricultor):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.callproc("sp_desactivar_agricultor", (id_agricultor,))
        conn.commit()
    finally:
        cursor.close()
        conn.close()

# ==============================
# 📌 Activar agricultor (estado = 1)
# ==============================
def activar_agricultor(id_agricultor):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.callproc("sp_activar_agricultor", (id_agricultor,))
        conn.commit()
    finally:
        cursor.close()
        conn.close()

# ==============================
# 📊 Obtener entregables por agricultor
# ==============================
def obtener_entregables_por_agricultor(id_agricultor):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT 
            variedad,
            jabas_entregadas,
            jabas_devueltas,
            saldo_jabas,
            total_kilos_bruto,
            total_kilos_neto,
            ultima_fecha,
            estado
        FROM vw_entregables_agricultor
        WHERE id_agricultor = %s
    """
    cursor.execute(query, (id_agricultor,))
    entregables = cursor.fetchall()
    cursor.close()
    conn.close()
    return entregables
