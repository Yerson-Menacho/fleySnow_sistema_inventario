import mysql.connector
from app.models import get_db_connection

def listar_categorias():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.callproc("sp_listar_categorias")
    resultado = []
    for res in cursor.stored_results():
        resultado = res.fetchall()
    cursor.close()
    conn.close()
    return resultado

def agregar_categoria(datos):
    # Validar longitud del código
    if len(datos['codigo_categoria']) > 5:
        raise ValueError("El código no puede tener más de 5 caracteres")

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.callproc("sp_insertar_categoria", (
            datos['codigo_categoria'], datos['nombre_categoria']
        ))
        conn.commit()
    except mysql.connector.IntegrityError as e:
        if "Duplicate entry" in str(e):
            raise ValueError("El código o nombre de la categoría ya existe.")
        else:
            raise
    finally:
        cursor.close()
        conn.close()

def actualizar_categoria(datos):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.callproc("sp_actualizar_categoria", (
        datos['id_categoria'], datos['codigo_categoria'], datos['nombre_categoria']
    ))
    conn.commit()
    cursor.close()
    conn.close()

def eliminar_categoria(id_categoria):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.callproc("sp_eliminar_categoria", (id_categoria,))
    conn.commit()
    cursor.close()
    conn.close()

def obtener_categoria(id_categoria):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM categorias WHERE id_categoria = %s", (id_categoria,))
    categoria = cursor.fetchone()
    cursor.close()
    conn.close()
    return categoria
