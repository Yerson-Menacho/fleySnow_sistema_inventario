import mysql.connector
from app.models import get_db_connection

def listar_variedades(id_categoria=None, codigo_categoria=None):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    try:
        if id_categoria:
            # 🔹 Filtrar por id_categoria directamente
            cur.execute("""
                SELECT 
                    v.id_variedad, 
                    v.codigo_variedad, 
                    v.nombre_variedad, 
                    v.id_categoria,
                    c.nombre_categoria
                FROM variedades v
                INNER JOIN categorias c ON v.id_categoria = c.id_categoria
                WHERE v.id_categoria = %s
                ORDER BY v.nombre_variedad
            """, (id_categoria,))
            variedades = cur.fetchall()

        elif codigo_categoria:
            # 🔹 Filtrar por código si se pasa
            cur.execute("""
                SELECT 
                    v.id_variedad, 
                    v.codigo_variedad, 
                    v.nombre_variedad, 
                    v.id_categoria,
                    c.nombre_categoria
                FROM variedades v
                INNER JOIN categorias c ON v.id_categoria = c.id_categoria
                WHERE c.codigo_categoria = %s
                ORDER BY v.nombre_variedad
            """, (codigo_categoria,))
            variedades = cur.fetchall()

        else:
            # 🔹 Sin filtro → usar el SP
            cur.callproc("sp_listar_variedades")
            for res in cur.stored_results():
                variedades = res.fetchall()
    finally:
        cur.close()
        conn.close()

    return variedades


def agregar_variedad(datos):
    # Validar longitud del código
    if len(datos['codigo_variedad']) > 5:
        raise ValueError("El código no puede tener más de 5 caracteres")

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.callproc("sp_insertar_variedad", (
            datos['codigo_variedad'], datos['nombre_variedad'], datos['id_categoria']
        ))
        conn.commit()
    except mysql.connector.IntegrityError as e:
        if "Duplicate entry" in str(e):
            raise ValueError("El código o nombre de la variedad ya existe.")
        else:
            raise
    finally:
        cursor.close()
        conn.close()

def actualizar_variedad(datos):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.callproc("sp_actualizar_variedad", (
        datos['id_variedad'], datos['codigo_variedad'], datos['nombre_variedad'], datos['id_categoria']
    ))
    conn.commit()
    cursor.close()
    conn.close()

def eliminar_variedad(id_variedad):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.callproc("sp_eliminar_variedad", (id_variedad,))
    conn.commit()
    cursor.close()
    conn.close()

def obtener_variedad(id_variedad):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM variedades WHERE id_variedad = %s", (id_variedad,))
    variedad = cursor.fetchone()
    cursor.close()
    conn.close()
    return variedad
