from app.models import get_db_connection
import mysql.connector

# ==============================
# 📌 Crear una nota de movimiento
# ==============================
def crear_nota_movimiento(id_tipo, referencia, id_usuario, id_origen, observacion):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.callproc("sp_crear_nota_movimiento", (
            id_tipo, referencia, id_usuario, id_origen, observacion
        ))
        conn.commit()

        cursor.execute("SELECT LAST_INSERT_ID() AS id_nota")
        id_nota = cursor.fetchone()["id_nota"]

        return {"id_nota": id_nota, "mensaje": "Nota creada correctamente"}

    except mysql.connector.Error as e:
        conn.rollback()
        raise ValueError(f"Error al crear nota de movimiento: {e}")
    finally:
        cursor.close()
        conn.close()


# ==============================
# 📌 Agregar detalle a una nota
# ==============================
def agregar_detalle_movimiento(id_nota, id_insumo, id_tipo, cantidad, unidad_medida):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.callproc("sp_agregar_detalle_movimiento", (
            id_nota, id_insumo, id_tipo, cantidad, unidad_medida
        ))

        id_movimiento = None
        for result in cursor.stored_results():
            row = result.fetchone()
            if row:
                id_movimiento = row["id_movimiento"]

        conn.commit()
        return {"id_movimiento": id_movimiento, "mensaje": "Detalle agregado correctamente"}

    except mysql.connector.Error as e:
        conn.rollback()
        raise ValueError(f"Error al agregar detalle: {e}")
    finally:
        cursor.close()
        conn.close()

# ==============================
# 📌 Listar notas de movimiento
# ==============================
def listar_notas_movimiento(p_q=None, p_id_tipo=None, p_estado=None, p_fecha_inicio=None, p_fecha_fin=None):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Si algo viene vacío o "", pásalo como None para que se traduzca a NULL
    params = [
        p_q if p_q not in ("", None) else None,
        p_id_tipo if p_id_tipo not in ("", None) else None,
        p_estado if p_estado not in ("", None) else None,
        p_fecha_inicio if p_fecha_inicio not in ("", None) else None,
        p_fecha_fin if p_fecha_fin not in ("", None) else None
    ]

    cursor.callproc("sp_listar_notas_movimiento", params)

    resultado = []
    for res in cursor.stored_results():
        resultado = res.fetchall()

    cursor.close()
    conn.close()
    return resultado

# ==============================
# 📌 Aprobar una nota de movimiento (impacta el stock)
# ==============================
def aprobar_nota_movimiento(id_nota):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.callproc("sp_aprobar_nota_movimiento", (id_nota,))
        conn.commit()
        return {"mensaje": f"Nota {id_nota} aprobada correctamente y stock actualizado."}
    except mysql.connector.Error as e:
        conn.rollback()
        raise ValueError(f"Error al aprobar nota: {e}")
    finally:
        cursor.close()
        conn.close()
        
# ==============================
# 📌 Actualizar estado de nota
# ==============================
def actualizar_estado_nota(id_nota, estado):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.callproc("sp_actualizar_estado_nota", (id_nota, estado))
        conn.commit()
    except mysql.connector.Error as e:
        conn.rollback()
        raise ValueError(f"Error al actualizar estado de nota: {e}")
    finally:
        cursor.close()
        conn.close()


# ==============================
# 📌 Listar salidas de jabas por agricultor
# ==============================
def listar_salidas_jabas(id_agricultor):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.callproc("sp_listar_salidas_jabas", (id_agricultor,))
        resultado = []
        for res in cursor.stored_results():
            resultado = res.fetchall()
        return resultado
    finally:
        cursor.close()
        conn.close()

# ==============================
# 📌 Registrar devolución de jabas
# ==============================
def registrar_devolucion_jabas(id_recepcion, id_agricultor, cantidad_devuelta):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.callproc("sp_registrar_devolucion_jabas", (
            id_recepcion, id_agricultor, cantidad_devuelta
        ))
        conn.commit()
    except mysql.connector.Error as e:
        conn.rollback()
        raise ValueError(f"Error al registrar devolución de jabas: {e}")
    finally:
        cursor.close()
        conn.close()

def kardex_insumo(id_insumo):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.callproc("sp_kardex_insumo", (id_insumo,))
        resultado = []
        for res in cursor.stored_results():
            resultado = res.fetchall()
        return resultado
    finally:
        cursor.close()
        conn.close()

def listar_origenes():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.callproc("sp_listar_origenes")
    origenes = []
    for result in cursor.stored_results():
        origenes = result.fetchall()
    cursor.close()
    conn.close()
    return origenes

def obtener_nota_por_id(id_nota):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.callproc("sp_obtener_nota_por_id", (id_nota,))
        for result in cursor.stored_results():
            return result.fetchone()
    finally:
        cursor.close()
        conn.close()

def obtener_detalles_por_nota(id_nota):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.callproc("sp_obtener_detalles_por_nota", (id_nota,))
        for result in cursor.stored_results():
            return result.fetchall()
    finally:
        cursor.close()
        conn.close()


# ==============================
# 📌 Actualizar cabecera de una nota
# ==============================

def actualizar_nota_movimiento(id_nota, id_tipo, referencia, id_usuario, id_origen, observacion, fecha):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.callproc("sp_actualizar_nota_movimiento", (
            id_nota, id_tipo, referencia, id_usuario, id_origen, observacion, fecha
        ))
        conn.commit()
    except mysql.connector.Error as e:
        conn.rollback()
        raise ValueError(f"Error al actualizar nota de movimiento: {e}")
    finally:
        cursor.close()
        conn.close()

# ==============================
# 📌 Eliminar detalles de una nota
# ==============================
def eliminar_detalles_movimiento(id_nota):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.callproc("sp_eliminar_detalles_movimiento", (id_nota,))
        conn.commit()
    except mysql.connector.Error as e:
        conn.rollback()
        raise ValueError(f"Error al eliminar detalles: {e}")
    finally:
        cursor.close()
        conn.close()

def obtener_nota_completa(id_nota):
    cabecera = obtener_nota_por_id(id_nota)
    if not cabecera:
        return None, None
    detalles = obtener_detalles_por_nota(id_nota)
    return cabecera, detalles

