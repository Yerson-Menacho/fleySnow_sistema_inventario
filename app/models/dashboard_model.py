# app/models/dashboard_model.py
from datetime import datetime, timedelta
from app.models import get_db_connection

# -------------------------
# Helper: formato fecha
# -------------------------
def _fecha_str(fecha):
    if hasattr(fecha, "strftime"):
        return fecha.strftime("%Y-%m-%d")
    return fecha

# -------------------------
# Total Insumos
# -------------------------
def total_insumos():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT COUNT(*) AS total FROM insumos")
    r = cur.fetchone()
    cur.close()
    conn.close()
    return r["total"] if r and r.get("total") is not None else 0

# -------------------------
# Insumos con stock bajo (stock_actual < stock_minimo)
# -------------------------
def insumos_stock_bajo():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT COUNT(*) AS total
        FROM insumos
        WHERE stock_actual < stock_minimo
    """)
    r = cur.fetchone()
    cur.close()
    conn.close()
    return r["total"] if r and r.get("total") is not None else 0

# -------------------------
# Insumos activos / descontinuados
# -------------------------
def insumos_activos_descontinuados():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT 
          SUM(CASE WHEN estado = 1 THEN 1 ELSE 0 END) AS activos,
          SUM(CASE WHEN estado = 0 THEN 1 ELSE 0 END) AS descontinuados
        FROM insumos
    """)
    r = cur.fetchone()
    cur.close()
    conn.close()
    return {
        "activos": int(r["activos"] or 0),
        "descontinuados": int(r["descontinuados"] or 0)
    }

# -------------------------
# Alertas pendientes (visto = 0)
# -------------------------
def alertas_pendientes():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT COUNT(*) AS total FROM alertas WHERE visto = 0")
    r = cur.fetchone()
    cur.close()
    conn.close()
    return r["total"] if r and r.get("total") is not None else 0

# -------------------------
# Total recepciones del mes
# -------------------------
def recepciones_mes(actual=True):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    today = datetime.now()
    first_day = today.replace(day=1).strftime("%Y-%m-%d")
    cur.execute("""
        SELECT COUNT(*) AS total 
        FROM recepcion_materia_prima
        WHERE DATE(fecha_recepcion) >= %s
    """, (first_day,))
    r = cur.fetchone()
    cur.close()
    conn.close()
    return r["total"] if r and r.get("total") is not None else 0

# -------------------------
# Stock por categoría -> devuelve labels + data
# -------------------------
def stock_por_categoria():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT c.nombre_categoria AS categoria, COALESCE(SUM(i.stock_actual),0) AS total_stock
        FROM categorias c
        LEFT JOIN insumos i ON i.id_categoria = c.id_categoria
        GROUP BY c.id_categoria
        ORDER BY total_stock DESC
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    labels = [r["categoria"] for r in rows]
    data = [int(r["total_stock"] or 0) for r in rows]
    return labels, data

def entradas_salidas_ultimos_dias(dias=30):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    end = datetime.now().date()
    start = end - timedelta(days=dias-1)

    cur.execute("""
        SELECT DATE(mi.fecha_movimiento) AS fecha,
               tm.nombre AS tipo,
               SUM(mi.cantidad) AS total
        FROM movimientos_inventario mi
        INNER JOIN tipo_movimiento tm ON tm.id_tipo = mi.id_tipo
        WHERE DATE(mi.fecha_movimiento) BETWEEN %s AND %s
        GROUP BY DATE(mi.fecha_movimiento), mi.id_tipo
        ORDER BY DATE(mi.fecha_movimiento)
    """, (start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    # preparar mapa de fecha -> entrada/salida
    fecha_map = {}
    for i in range(dias):
        d = start + timedelta(days=i)
        key = d.strftime("%Y-%m-%d")
        fecha_map[key] = {"entrada": 0, "salida": 0}

    for r in rows:
        f = r["fecha"].strftime("%Y-%m-%d") if hasattr(r["fecha"], "strftime") else str(r["fecha"])
        tipo = (r["tipo"] or "").lower()
        if "entrada" in tipo:
            fecha_map[f]["entrada"] += float(r["total"] or 0)
        else:
            fecha_map[f]["salida"] += float(r["total"] or 0)

    labels = list(fecha_map.keys())
    entradas = [fecha_map[k]["entrada"] for k in labels]
    salidas = [fecha_map[k]["salida"] for k in labels]

    return labels, entradas, salidas

# -------------------------
# Peso neto por variedad (últimos N días)
# -------------------------
def peso_neto_por_variedad(dias=30, limit=10):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    end = datetime.now().date()
    start = end - timedelta(days=dias-1)
    cur.execute("""
        SELECT v.nombre_variedad AS variedad, COALESCE(SUM(d.peso_neto),0) AS total_neto
        FROM detalle_recepcion_materia_prima d
        INNER JOIN variedades v ON v.id_variedad = d.id_variedad
        INNER JOIN recepcion_materia_prima r ON r.id_recepcion = d.id_recepcion
        WHERE DATE(r.fecha_recepcion) BETWEEN %s AND %s
        GROUP BY v.id_variedad
        ORDER BY total_neto DESC
        LIMIT %s
    """, (start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d"), limit))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    labels = [r["variedad"] for r in rows]
    data = [float(r["total_neto"] or 0) for r in rows]
    return labels, data

# -------------------------
# Top agricultores por peso neto recibido (últimos N días)
# -------------------------
def top_agricultores_por_peso(dias=30, limit=10):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    end = datetime.now().date()
    start = end - timedelta(days=dias-1)
    cur.execute("""
        SELECT a.nombres AS nombre, a.apellidos AS apellido, COALESCE(SUM(d.peso_neto),0) AS total_neto
        FROM detalle_recepcion_materia_prima d
        INNER JOIN recepcion_materia_prima r ON r.id_recepcion = d.id_recepcion
        INNER JOIN agricultores a ON a.id_agricultor = r.id_agricultor
        WHERE DATE(r.fecha_recepcion) BETWEEN %s AND %s
        GROUP BY a.id_agricultor
        ORDER BY total_neto DESC
        LIMIT %s
    """, (start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d"), limit))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"nombre": f"{r['nombre']} {r['apellido']}", "peso": float(r["total_neto"] or 0)} for r in rows]

# -------------------------
# Jabas entregadas vs devueltas (últimos N días)
# -------------------------
def jabas_entregadas_devueltas(dias=30):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    end = datetime.now().date()
    start = end - timedelta(days=dias-1)
    cur.execute("""
        SELECT DATE(fecha) AS fecha, tipo_movimiento, SUM(cantidad_jabas) AS total
        FROM control_jabas_agricultor
        WHERE DATE(fecha) BETWEEN %s AND %s
        GROUP BY DATE(fecha), tipo_movimiento
        ORDER BY DATE(fecha)
    """, (start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    # map fechas
    fecha_map = {}
    for i in range(dias):
        d = start + timedelta(days=i)
        k = d.strftime("%Y-%m-%d")
        fecha_map[k] = {"entrega": 0, "devolucion": 0}

    for r in rows:
        f = r["fecha"].strftime("%Y-%m-%d") if hasattr(r["fecha"], "strftime") else str(r["fecha"])
        t = (r["tipo_movimiento"] or "").lower()
        if "entrega" in t:
            fecha_map[f]["entrega"] += int(r["total"] or 0)
        else:
            fecha_map[f]["devolucion"] += int(r["total"] or 0)

    labels = list(fecha_map.keys())
    entregas = [fecha_map[k]["entrega"] for k in labels]
    devoluciones = [fecha_map[k]["devolucion"] for k in labels]
    return labels, entregas, devoluciones

# -------------------------
# Agricultores con jabas pendientes (entrega - devolucion > 0)
# -------------------------
def agricultores_jabas_pendientes():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT 
            a.id_agricultor, 
            a.nombres, 
            a.apellidos,
            COALESCE(SUM(CASE WHEN c.tipo_movimiento='entrega' THEN c.cantidad_jabas ELSE 0 END),0) AS entregadas,
            COALESCE(SUM(CASE WHEN c.tipo_movimiento='devolucion' THEN c.cantidad_jabas ELSE 0 END),0) AS devueltas
        FROM control_jabas_agricultor c
        INNER JOIN agricultores a ON a.id_agricultor = c.id_agricultor
        GROUP BY a.id_agricultor
        HAVING 
            COALESCE(SUM(CASE WHEN c.tipo_movimiento='entrega' THEN c.cantidad_jabas ELSE 0 END),0)
            - 
            COALESCE(SUM(CASE WHEN c.tipo_movimiento='devolucion' THEN c.cantidad_jabas ELSE 0 END),0)
            > 0
        ORDER BY 
            COALESCE(SUM(CASE WHEN c.tipo_movimiento='entrega' THEN c.cantidad_jabas ELSE 0 END),0)
            - 
            COALESCE(SUM(CASE WHEN c.tipo_movimiento='devolucion' THEN c.cantidad_jabas ELSE 0 END),0)
            DESC
        LIMIT 20
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        {
            "id": r["id_agricultor"],
            "nombre": f"{r['nombres']} {r['apellidos']}",
            "pendientes": int((r["entregadas"] or 0) - (r["devueltas"] or 0))
        } 
        for r in rows
    ]


# -------------------------
# Últimas actividades (log_actividad)
# -------------------------
def ultimas_actividades(limit=10):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT la.fecha, u.nombre_completo AS usuario, la.accion, la.descripcion
        FROM log_actividad la
        LEFT JOIN usuarios u ON u.id_usuario = la.id_usuario
        ORDER BY la.fecha DESC
        LIMIT %s
    """, (limit,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

# -------------------------
# Actividad por día (últimos N días)
# -------------------------
def actividad_por_dia(dias=30):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    end = datetime.now().date()
    start = end - timedelta(days=dias-1)
    cur.execute("""
        SELECT DATE(fecha) AS fecha, COUNT(*) AS total
        FROM log_actividad
        WHERE DATE(fecha) BETWEEN %s AND %s
        GROUP BY DATE(fecha)
        ORDER BY DATE(fecha)
    """, (start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    fecha_map = {}
    for i in range(dias):
        d = start + timedelta(days=i)
        fecha_map[d.strftime("%Y-%m-%d")] = 0
    for r in rows:
        f = r["fecha"].strftime("%Y-%m-%d") if hasattr(r["fecha"], "strftime") else str(r["fecha"])
        fecha_map[f] = int(r["total"] or 0)
    labels = list(fecha_map.keys())
    data = [fecha_map[k] for k in labels]
    return labels, data

# -------------------------
# Insumos próximos a vencer (dentro de N días)
# -------------------------
def insumos_proximo_vencer(dias=30):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT id_insumo, nombre_insumo, fecha_vencimiento, stock_actual, unidad_medida
        FROM insumos
        WHERE fecha_vencimiento IS NOT NULL
          AND DATE(fecha_vencimiento) BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL %s DAY)
        ORDER BY fecha_vencimiento
        LIMIT 50
    """, (dias,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

# -------------------------
# Últimos movimientos (simples)
# -------------------------
def ultimos_movimientos(limit=10):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT m.fecha_movimiento AS fecha, i.nombre_insumo AS insumo, tm.nombre AS tipo, m.cantidad, u.nombre_completo AS usuario
        FROM movimientos_inventario m
        LEFT JOIN insumos i ON i.id_insumo = m.id_insumo
        LEFT JOIN tipo_movimiento tm ON tm.id_tipo = m.id_tipo
        LEFT JOIN nota_movimiento n ON n.id_nota = m.id_nota
        LEFT JOIN usuarios u ON u.id_usuario = n.id_usuario
        ORDER BY m.fecha_movimiento DESC
        LIMIT %s
    """, (limit,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows
