from flask import Flask, redirect, session, url_for
from app.models import get_db_connection, close_db_connection

def tiene_permiso(codigo_accion):
    # 👑 Admin siempre tiene acceso
    if session.get("id_rol") == 1:
        return True
    
    # 👤 Usuario normal → validar permisos por código
    permisos = session.get("permisos", [])
    return codigo_accion in permisos


def create_app():
    app = Flask(__name__)

    # Clave 
    app.secret_key = "e9a3b7f4e6c84b10c4cbd15a9a2b57f8d3e0a1c96d48a772a09c1f05db5af123"  

    # Configuración de BD
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = ''
    app.config['MYSQL_DB'] = 'fley_snow_db'

    # Cerrar conexión
    app.teardown_appcontext(close_db_connection)

    @app.route('/conexion')
    def conexion():
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT DATABASE();")
        result = cursor.fetchone()
        return f"¡Conectado a la base de datos: {result[0]}!"

    # Registrar blueprints
    from app.routes.insumos_routes import insumos_bp
    app.register_blueprint(insumos_bp)

    from app.routes.categorias_routes import categorias_bp
    app.register_blueprint(categorias_bp)

    from app.routes.variedades_routes import variedades_bp
    app.register_blueprint(variedades_bp)

    from app.routes.movimientos_routes import movimientos_bp
    app.register_blueprint(movimientos_bp)

    from app.routes.reportes.reportes_usuarios import reportes_bp
    app.register_blueprint(reportes_bp)
    
    from app.routes.usuarios_routes import usuarios_bp
    app.register_blueprint(usuarios_bp)

    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)

    from app.routes.permisos_routes import permisos_bp
    app.register_blueprint(permisos_bp)

    from app.routes.agricultores_routes import agricultores_bp
    app.register_blueprint(agricultores_bp)

    from app.routes.dashboard_routes import dashboard_bp
    app.register_blueprint(dashboard_bp)

    from app.routes.recepcion_routes import recepcion_bp
    app.register_blueprint(recepcion_bp, url_prefix='/recepcion')

    app.jinja_env.globals.update(tiene_permiso=tiene_permiso)

    @app.route('/')
    def home():
        if 'usuario_id' not in session:
            return redirect(url_for('usuarios.login'))
        return redirect(url_for('usuarios.index'))

    return app
