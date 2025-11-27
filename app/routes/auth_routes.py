from app.models.categorias_model import listar_categorias
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import get_db_connection
from app.models.permisos_model import obtener_permisos_usuario
from app.models.usuarios_model import obtener_usuario_por_dni
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__)

# Página principal -> redirige a login
@auth_bp.route('/')
def index():
    return redirect(url_for('auth.login'))

# Login
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        dni = request.form['dni']
        contrasena = request.form['contrasena']

        usuario = obtener_usuario_por_dni(dni)
        if usuario and check_password_hash(usuario['contrasena'], contrasena):
            # ✅ Actualizar campo ultimo_login al iniciar sesión
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.callproc("sp_actualizar_ultimo_login", [usuario['id_usuario']])
            conn.commit()
            cursor.close()
            conn.close()
            # Guardamos datos en sesión
            session['usuario_id'] = usuario['id_usuario']
            session['nombre'] = usuario['nombre_completo']
            session['id_rol'] = int(usuario['id_rol'])

            # ✅ Guardamos solo permisos activos (permitido = 1)
            permisos = obtener_permisos_usuario(usuario['id_usuario'])
            session['permisos'] = [
                p['codigo'] for p in permisos if int(p.get('permitido', 0)) == 1
            ]

            # Debug para verificar la sesión cargada
            print(">>> SESIÓN INICIADA:", dict(session))

            flash("✅ Bienvenido " + usuario['nombre_completo'], "success")
            return redirect(url_for('auth.home'))
        else:
            flash("⚠️ DNI o contraseña incorrectos.", "danger")

    return render_template('auth/login.html')

# Home (panel principal después del login)
@auth_bp.route('/home')
def home():
    if "usuario_id" not in session:
        flash("⚠️ Debes iniciar sesión.", "warning")
        return redirect(url_for("auth.login"))

    return redirect(url_for("dashboard.dashboard_home"))

# Logout
@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("Sesión cerrada correctamente.", "info")
    return redirect(url_for('auth.login'))


