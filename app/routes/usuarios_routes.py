from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.models.usuarios_model import (
    listar_usuarios, insertar_usuario, obtener_usuario,
    actualizar_usuario, cambiar_contrasena, obtener_usuario_por_dni
)
from app.models.roles_model import listar_roles
from app.utils.auth import  permiso_de_admin

usuarios_bp = Blueprint('usuarios', __name__)

# ✅ Listado de usuarios
@usuarios_bp.route('/usuarios')
@permiso_de_admin('usuarios.ver')  # Ver usuario
def index():
    usuarios = listar_usuarios()
    return render_template('usuarios/index.html', usuarios=usuarios)

# ✅ Registrar usuario (solo admin puede asignar roles)
@usuarios_bp.route('/usuarios/nuevo', methods=['GET', 'POST'])
@permiso_de_admin('usuarios.crear')  # nuevo usuairo
def nuevo_usuario():
    if request.method == 'POST':
        try:
            datos = {
                'nombre_completo': request.form['nombre_completo'],
                'dni': request.form['dni'],
                'contrasena': request.form['contrasena'],
                'email': request.form['email'],
                'telefono': request.form.get('telefono') or None,
                'id_rol': int(request.form['id_rol'])
            }
            insertar_usuario(datos)
            flash("✅ Usuario registrado con éxito.", "success")
            return redirect(url_for('usuarios.index'))
        except ValueError as e:
            flash(str(e), "danger")
            return redirect(url_for('usuarios.nuevo_usuario'))

    roles = listar_roles()
    return render_template('usuarios/registrar.html', roles=roles)

# ✅ Editar usuario (solo admin puede cambiar rol y estado)
@usuarios_bp.route('/usuarios/editar/<int:id_usuario>', methods=['GET', 'POST'])
@permiso_de_admin('usuarios.editar')  # Editar usuairo
def editar_usuario(id_usuario):
    usuario = obtener_usuario(id_usuario)
    if not usuario:
        flash("⚠️ Usuario no encontrado.", "warning")
        return redirect(url_for('usuarios.index'))

    if request.method == 'POST':
        try:
            datos = {
                'id_usuario': id_usuario,
                'nombre_completo': request.form['nombre_completo'],
                'dni': request.form['dni'],
                'email': request.form['email'],
                'telefono': request.form.get('telefono') or None,
                'id_rol': int(request.form['id_rol']),
                'estado': int(request.form['estado'])
            }
            actualizar_usuario(datos)
            flash("✅ Usuario actualizado con éxito.", "success")
            return redirect(url_for('usuarios.index'))
        except ValueError as e:
            flash(str(e), "danger")
            return redirect(url_for('usuarios.editar_usuario', id_usuario=id_usuario))

    roles = listar_roles()
    return render_template('usuarios/editar.html', usuario=usuario, roles=roles)

# ✅ Cambiar contraseña (puede hacerlo admin o el mismo usuario)
@usuarios_bp.route('/usuarios/cambiar_password/<int:id_usuario>', methods=['GET', 'POST'])
@permiso_de_admin('usuarios.cambiar_pass')  # Cambiar contraseña del usuairo
def cambiar_password(id_usuario):
    usuario = obtener_usuario(id_usuario)
    if not usuario:
        flash("⚠️ Usuario no encontrado.", "warning")
        return redirect(url_for('usuarios.index'))

    if request.method == 'POST':
        contrasena = request.form['contrasena']
        confirmar = request.form['confirmar']

        if contrasena != confirmar:
            flash("⚠️ Las contraseñas no coinciden.", "danger")
            return redirect(url_for('usuarios.cambiar_password', id_usuario=id_usuario))

        try:
            cambiar_contrasena(id_usuario, contrasena)
            flash("✅ Contraseña actualizada con éxito.", "success")
            return redirect(url_for('usuarios.index'))
        except ValueError as e:
            flash(str(e), "danger")
            return redirect(url_for('usuarios.cambiar_password', id_usuario=id_usuario))

    return render_template('usuarios/cambiar_password.html', usuario=usuario)

# ✅ Endpoint para buscar usuario por DNI (para autocomplete)
@usuarios_bp.route('/api/usuario/<dni>', methods=['GET'])
@permiso_de_admin()
def api_usuario_por_dni(dni):
    usuario = obtener_usuario_por_dni(dni) 
    if usuario:
        return jsonify({
            "nombre_completo": usuario["nombre_completo"],
            "email": usuario["email"],
            "telefono": usuario["telefono"],
            "id_rol": usuario["id_rol"]
        })
    return jsonify({"error": "No encontrado"}), 404

# ==============================
# 🔍 Endpoint AJAX para Select2 - usuarios
# ==============================
@usuarios_bp.route('/usuarios/buscar_usuario')
def buscar_usuarios():
    q = request.args.get("q", "").strip().lower()
    usuarios = listar_usuarios()

    if q:
        usuarios = [
            u for u in usuarios
            if q in (u.get("nombre_completo") or "").lower()
            or q in (u.get("dni") or "").lower()
            or q in str(u.get("id_usuario"))
        ]

    # Renderiza solo las filas (sin el layout completo)
    return render_template('usuarios/_tabla_usuarios.html', usuarios=usuarios)
