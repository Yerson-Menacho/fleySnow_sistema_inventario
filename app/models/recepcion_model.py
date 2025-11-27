from app.models import get_db_connection
import mysql.connector

# ==========================================================
# 📌 Crear recepción (CABECERA)
# ==========================================================

def crear_recepcion(id_nota_salida, id_agricultor, fecha_recepcion, observaciones, id_responsable):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.callproc("sp_crear_recepcion_materia_prima", (
            id_nota_salida, id_agricultor, fecha_recepcion, observaciones, id_responsable
        ))
        conn.commit()

        result = None
        for stored in cursor.stored_results():
            rows = stored.fetchall()
            if rows:
                result = rows[0]
                break

        if not result:
            cursor.execute("SELECT LAST_INSERT_ID() AS id_recepcion")
            row = cursor.fetchone()
            id_recepcion = row["id_recepcion"] if row else None
            if id_recepcion is None:
                raise ValueError("No se pudo obtener id_recepcion después de crear la cabecera.")
            result = {"id_recepcion": id_recepcion}
        return result

    except mysql.connector.Error as e:
        conn.rollback()
        raise ValueError(f"Error al crear recepción: {e}")
    finally:
        cursor.close()
        conn.close()


# ==========================================================
# 📋 Agregar detalle de recepción
# ==========================================================
def agregar_detalle_recepcion(id_recepcion, id_variedad, lote, peso_bruto, cantidad_jabas, peso_neto, unidad_medida):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.callproc('sp_agregar_detalle_recepcion', (
            id_recepcion, id_variedad, lote, peso_bruto, cantidad_jabas, peso_neto, unidad_medida
        ))
        conn.commit()
    except mysql.connector.Error as e:
        conn.rollback()
        raise ValueError(f"Error al agregar detalle: {e}")
    finally:
        cursor.close()
        conn.close()

# ==========================================================
# 📋 Listar todas las recepciones
# ==========================================================
def listar_recepciones(p_q=None, p_id_agricultor=None, p_estado=None, p_fecha_inicio=None, p_fecha_fin=None):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    params = [
        p_q if p_q not in ("", None) else None,
        p_id_agricultor if p_id_agricultor not in ("", None) else None,
        p_estado if p_estado not in ("", None) else None,
        p_fecha_inicio if p_fecha_inicio not in ("", None) else None,
        p_fecha_fin if p_fecha_fin not in ("", None) else None
    ]

    cursor.callproc("sp_listar_recepciones_detalle", params)

    resultado = []
    for res in cursor.stored_results():
        resultado = res.fetchall()

    cursor.close()
    conn.close()
    return resultado

# ==========================================================
# 🔍 Obtener cabecera de una recepción por ID
# ==========================================================
def obtener_recepcion_por_id(id_recepcion):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.callproc("sp_obtener_recepcion_por_id", (id_recepcion,))
        for res in cursor.stored_results():
            return res.fetchone()
    finally:
        cursor.close()
        conn.close()


# ==========================================================
# 🔍 Obtener detalles de una recepción
# ==========================================================
def obtener_detalles_recepcion(id_recepcion):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.callproc("sp_detalle_recepcion", (id_recepcion,))
        for res in cursor.stored_results():
            return res.fetchall()
    finally:
        cursor.close()
        conn.close()


# ==========================================================
# ✏️ Actualizar cabecera de recepción
# ==========================================================
def actualizar_recepcion(id_recepcion, id_agricultor, id_responsable, observaciones, estado):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.callproc("sp_actualizar_recepcion", (
            id_recepcion, id_agricultor, observaciones, id_responsable, estado
        ))
        conn.commit()
    except mysql.connector.Error as e:
        conn.rollback()
        raise ValueError(f"Error al actualizar recepción: {e}")
    finally:
        cursor.close()
        conn.close()

# ==========================================================
# 🗑️ Eliminar actualizar y anular detalles de recepcion
# ==========================================================
def eliminar_detalles_recepcion(id_recepcion):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.callproc("sp_eliminar_detalles_recepcion", (id_recepcion,))
        conn.commit()
    except mysql.connector.Error as e:
        conn.rollback()
        raise ValueError(f"Error al eliminar detalles: {e}")
    finally:
        cursor.close()
        conn.close()

def actualizar_detalle_recepcion(id_detalle, id_variedad, lote, peso_bruto, cantidad_jabas, peso_neto, unidad_medida):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.callproc("sp_actualizar_detalle_recepcion", (
            id_detalle, id_variedad, lote, peso_bruto, cantidad_jabas, peso_neto, unidad_medida
        ))
        conn.commit()
    except mysql.connector.Error as e:
        conn.rollback()
        raise ValueError(f"Error al actualizar detalle: {e}")
    finally:
        cursor.close()
        conn.close()

def eliminar_detalle_recepcion(id_detalle):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.callproc("sp_eliminar_detalle_recepcion", (id_detalle,))
        conn.commit()
    except mysql.connector.Error as e:
        conn.rollback()
        raise ValueError(f"Error al eliminar detalle: {e}")
    finally:
        cursor.close()
        conn.close()



# ==========================================================
# 🔄 Cambiar estado (pendiente, aprobado, anulado)
# ==========================================================
def actualizar_estado_recepcion(id_recepcion, estado):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.callproc("sp_actualizar_estado_recepcion", (id_recepcion, estado))
        conn.commit()
    except mysql.connector.Error as e:
        conn.rollback()
        raise ValueError(f"Error al actualizar estado: {e}")
    finally:
        cursor.close()
        conn.close()


# ==========================================================
# ✅ Aprobar recepción (actualiza stock, cambia estado)
# ==========================================================
def aprobar_recepcion(id_recepcion):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.callproc("sp_aprobar_recepcion", (id_recepcion,))
        conn.commit()
    except mysql.connector.Error as e:
        conn.rollback()
        raise ValueError(f"Error al aprobar recepción: {e}")
    finally:
        cursor.close()
        conn.close()

def obtener_notas_salida(id_agricultor):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    # Llamar al procedimiento almacenado
    cur.callproc('sp_control_jabas_agricultor', (id_agricultor,))

    # Recuperar los resultados del procedimiento
    notas = []
    for result in cur.stored_results():
        notas = result.fetchall()

    cur.close()
    conn.close()

    # Asegurar que los campos numéricos estén como float
    for n in notas:
        n['saldo_jabas'] = float(n.get('saldo_jabas') or 0)
        n['cantidad_salida'] = float(n.get('cantidad_salida') or 0)
        n['cantidad_devolucion'] = float(n.get('cantidad_devolucion') or 0)

    return notas

def obtener_recepcion_completa(id_recepcion):
    cabecera = obtener_recepcion_por_id(id_recepcion)
    if not cabecera:
        return None, None

    detalles = obtener_detalles_recepcion(id_recepcion)
    return cabecera, detalles