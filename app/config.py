def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='tu_clave',
        database='inventario_db'
    )
