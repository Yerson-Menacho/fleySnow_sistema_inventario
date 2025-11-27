from app.models import get_db_connection

def listar_tipos_movimiento():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id_tipo, nombre FROM tipo_movimiento")
    resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultado
