import mysql.connector
from app.models import get_db_connection

# ==============================
# LISTAR INSUMOS
# ==============================
def listar_insumos(p_q=None, p_id_categoria=None, p_id_variedad=None, p_estado=None, p_fecha_inicio=None, p_fecha_fin=None):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Llamada al procedimiento almacenado con los 6 parámetros
    cursor.callproc("sp_listar_insumos", [p_q, p_id_categoria, p_id_variedad, p_estado, p_fecha_inicio, p_fecha_fin])
    
    resultado = []
    for res in cursor.stored_results():
        resultado = res.fetchall()
    
    cursor.close()
    conn.close()
    return resultado

# ==============================
# AGREGAR INSUMO
# ==============================
def agregar_insumo(datos):
    # Validar longitud del código
    if len(datos['codigo_insumo']) > 5:
        raise ValueError("El código no puede tener más de 5 caracteres")

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.callproc("sp_insertar_insumo", (
            datos['codigo_insumo'], datos['nombre_insumo'], datos['id_categoria'],
            datos['id_variedad'], datos['stock_actual'], datos['unidad_medida'],
            datos['fecha_vencimiento'], datos['descripcion'], datos['estado']
        ))
        conn.commit()
    except mysql.connector.IntegrityError as e:
        if "Duplicate entry" in str(e):
            raise ValueError("El código o nombre de insumo ya existe.")
        else:
            raise
    finally:
        cursor.close()
        conn.close()

# ==============================
# ACTUALIZAR INSUMO
# ==============================
def actualizar_insumo(datos):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.callproc("sp_actualizar_insumo", (
        datos['id_insumo'],
        datos['codigo_insumo'], 
        datos['nombre_insumo'],
        datos['id_categoria'], 
        datos['id_variedad'], 
        datos['stock_actual'],
        datos['unidad_medida'], 
        datos['fecha_vencimiento'], 
        datos['descripcion']
    ))
    conn.commit()
    cursor.close()
    conn.close()

# ==============================
# CAMBIAR ESTADO (ACTIVAR/DESACTIVAR)
# ==============================
def cambiar_estado(id_insumo, nuevo_estado):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.callproc("sp_cambiar_estado_insumo", (id_insumo, nuevo_estado))
    conn.commit()
    cursor.close()
    conn.close()

# ==============================
# OBTENER INSUMO POR ID
# ==============================
def obtener_insumo(id_insumo):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.callproc("sp_obtener_insumo", (id_insumo,))
    insumo = None
    for res in cursor.stored_results():
        insumo = res.fetchone()
    cursor.close()
    conn.close()
    return insumo

# ==============================
# LISTAR STOCK BAJO
# ==============================
def listar_insumos_stock_bajo():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.callproc("sp_insumos_stock_bajo")
    resultado = []
    for res in cursor.stored_results():
        resultado = res.fetchall()
    cursor.close()
    conn.close()
    return resultado

def listar_insumos_con_filtros(q=None):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Llamamos al SP pasando los parámetros
    cursor.callproc('sp_listar_insumos', [q or None, None, None, None, None, None])

    resultado = []
    for res in cursor.stored_results():
        resultado = res.fetchall()

    cursor.close()
    conn.close()
    return resultado
