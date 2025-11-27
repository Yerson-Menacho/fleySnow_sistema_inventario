from pydoc import text
from app.models import get_db_connection

def listar_usuarios_reporte(filtros):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    q = filtros.get("q")
    if q:
        q = q.strip().lower()
    else:
        q = None

    id_rol = filtros.get("id_rol")
    id_rol = int(id_rol) if id_rol and str(id_rol).isdigit() else None

    estado = filtros.get("estado")
    if estado in [None, "", "todos"]:
        estado = None
    else:
        estado = int(estado)

    fecha_inicio = filtros.get("fecha_inicio") or None
    fecha_fin = filtros.get("fecha_fin") or None

    cursor.callproc("sp_listar_usuarios", [q, id_rol, estado, fecha_inicio, fecha_fin])

    data = []
    for result in cursor.stored_results():
        data = result.fetchall()

    for u in data:
        if "nombre_rol" not in u and "rol" in u:
            u["nombre_rol"] = u["rol"]

    for u in data:
        if u.get("ultimo_login"):
            u["ultimo_login"] = u["ultimo_login"].strftime("%Y-%m-%d")
        if u.get("fecha_creacion"):
            u["fecha_creacion"] = u["fecha_creacion"].strftime("%Y-%m-%d")


    cursor.close()
    conn.close()
    return data

def listar_roles():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id_rol, nombre_rol FROM roles ORDER BY nombre_rol")
    roles = cursor.fetchall()
    cursor.close()
    conn.close()
    return roles

def listar_insumos_reporte(filtros):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    q = filtros.get("q")
    if q:
        q = q.strip().lower()
    else:
        q = None

    id_categoria = filtros.get("id_categoria")
    id_categoria = int(id_categoria) if id_categoria and str(id_categoria).isdigit() else None

    id_variedad = filtros.get("id_variedad")
    id_variedad = int(id_variedad) if id_variedad and str(id_variedad).isdigit() else None

    estado = filtros.get("estado")
    if estado in [None, "", "todos"]:
        estado = None
    else:
        estado = str(estado)  # puede ser '1' o '0'

    fecha_inicio = filtros.get("fecha_inicio") or None
    fecha_fin = filtros.get("fecha_fin") or None

    # --- Llamada al procedimiento almacenado ---
    cursor.callproc("sp_listar_insumos", [q, id_categoria, id_variedad, estado, fecha_inicio, fecha_fin])

    data = []
    for result in cursor.stored_results():
        data = result.fetchall()

    # --- Formateo de fechas ---
    for i in data:
        if i.get("fecha_ingreso"):
            i["fecha_ingreso"] = i["fecha_ingreso"].strftime("%Y-%m-%d")
        if i.get("fecha_vencimiento"):
            i["fecha_vencimiento"] = i["fecha_vencimiento"].strftime("%Y-%m-%d")

    cursor.close()
    conn.close()
    return data

def listar_agricultores_reporte(filtros):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # 🔍 Búsqueda general
    q = filtros.get("q")
    q = q.strip().lower() if q else None

    # ⚙️ Estado ('Activo', 'Inactivo', 'todos')
    estado = filtros.get("estado")
    if not estado or estado.lower() in ["", "todos"]:
        estado = None
    else:
        estado = estado.capitalize()  # Normaliza formato

    # 📅 Fechas
    fecha_inicio = filtros.get("fecha_inicio") or None
    fecha_fin = filtros.get("fecha_fin") or None

    # 🧠 Llamar al procedimiento almacenado
    cursor.callproc("sp_listar_agricultores", [q, estado, fecha_inicio, fecha_fin])

    data = []
    for result in cursor.stored_results():
        data = result.fetchall()

    # 🔄 Formatear fechas
    for a in data:
        if a.get("fecha_registro"):
            a["fecha_registro"] = a["fecha_registro"].strftime("%Y-%m-%d")

    cursor.close()
    conn.close()

    return data

def obtener_reporte_materia_prima(fecha_desde=None, fecha_hasta=None, id_variedad=None, id_agricultor=None, agrupacion='dia'):

    # 👇 definimos cómo se agrupa en SQL (clave para el GROUP BY)
    agrup_map_sql = {
        'dia': "DATE(r.fecha_recepcion)",
        'semana': "YEARWEEK(r.fecha_recepcion, 1)",
        'mes': "DATE_FORMAT(r.fecha_recepcion, '%Y-%m')",
        'variedad': None
    }

    # 👇 y cómo se mostrará el texto del periodo (para visualización)
    agrup_map_display = {
        'dia': "DATE_FORMAT(r.fecha_recepcion, '%d/%m/%Y')",
        'semana': "CONCAT('Semana ', LPAD(WEEK(r.fecha_recepcion, 1), 2, '0'), '/', YEAR(r.fecha_recepcion))",
        'mes': "CONCAT('Mes ', DATE_FORMAT(r.fecha_recepcion, '%m/%Y'))"
    }

    periodo_expr_sql = agrup_map_sql.get(agrupacion, agrup_map_sql['dia'])
    periodo_expr_display = agrup_map_display.get(agrupacion, agrup_map_display['dia'])

    sql = "SELECT "

    if agrupacion != 'variedad':
        sql += f" {periodo_expr_display} AS periodo,"

    sql += """
        v.id_variedad AS id_variedad,
        v.nombre_variedad AS variedad,
        COALESCE(SUM(d.peso_bruto), 0) AS total_bruto,
        COALESCE(SUM(d.cantidad_jabas), 0) AS total_jabas,
        COUNT(DISTINCT r.id_recepcion) AS recepciones_count
        FROM recepcion_materia_prima r
        LEFT JOIN detalle_recepcion_materia_prima d ON r.id_recepcion = d.id_recepcion
        LEFT JOIN variedades v ON d.id_variedad = v.id_variedad
        WHERE 1=1
    """

    params = []
    if fecha_desde:
        sql += " AND DATE(r.fecha_recepcion) >= %s"
        params.append(fecha_desde)
    if fecha_hasta:
        sql += " AND DATE(r.fecha_recepcion) <= %s"
        params.append(fecha_hasta)
    if id_variedad not in (None, '', '0'):
        sql += " AND v.id_variedad = %s"
        params.append(id_variedad)
    if id_agricultor not in (None, '', '0'):
        sql += " AND r.id_agricultor = %s"
        params.append(id_agricultor)

    if agrupacion == 'variedad':
        sql += " GROUP BY v.id_variedad, v.nombre_variedad"
        sql += " ORDER BY v.nombre_variedad ASC"
    else:
        sql += f" GROUP BY {periodo_expr_sql}, v.id_variedad, v.nombre_variedad"
        sql += f" ORDER BY {periodo_expr_sql} DESC, v.nombre_variedad ASC"

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(sql, tuple(params))
        results = cursor.fetchall()
        for row in results:
            row['total_bruto'] = float(row.get('total_bruto') or 0)
            row['total_jabas'] = float(row.get('total_jabas') or 0)
            row['recepciones_count'] = int(row.get('recepciones_count') or 0)
        return results
    finally:
        cursor.close()
        conn.close()
