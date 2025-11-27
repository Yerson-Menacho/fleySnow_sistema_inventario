from flask import Blueprint, render_template, redirect, request, url_for, flash
from app.models.agricultores_model import (
    activar_agricultor, listar_agricultores, agregar_agricultor, obtener_agricultor,
    actualizar_agricultor, desactivar_agricultor, obtener_entregables_por_agricultor
)
from app.utils.auth import permiso_de_admin  # Restricción de permisos

agricultores_bp = Blueprint('agricultores', __name__)

# ==============================
# 📌 Listado de Agricultores
# ==============================
@agricultores_bp.route('/agricultores')
@permiso_de_admin('agricultores.ver')  # Permiso: gestionar agricultores
def index():
    agricultores = listar_agricultores()
    return render_template('agricultores/index.html', agricultores=agricultores)

# ==============================
# 📌 Nuevo Agricultor
# ==============================
@agricultores_bp.route('/agricultores/nuevo', methods=['GET', 'POST'])
@permiso_de_admin('agricultores.crear')  # Permiso: crear agricultor
def nuevo_agricultor():
    if request.method == 'POST':
        datos = {
            'codigo_agricultor': request.form['codigo_agricultor'].strip(),
            'dni': request.form['dni'].strip(),
            'nombres': request.form['nombres'].strip(),
            'apellidos': request.form['apellidos'].strip(),
            'telefono': request.form['telefono'].strip(),
            'direccion': request.form['direccion'].strip(),
            'correo': request.form['correo'].strip(),
            'zona': request.form['zona'].strip(),
            'cultivo_principal': request.form['cultivo_principal'].strip()
        }
        try:
            agregar_agricultor(datos)
            flash("✅ Agricultor agregado correctamente.", "success")
            return redirect(url_for('agricultores.index'))
        except ValueError as e:
            flash(str(e), "danger")
            return render_template('agricultores/form.html', agricultor=None)

    return render_template('agricultores/form.html', agricultor=None)

# ==============================
# 📌 Editar Agricultor
# ==============================
@agricultores_bp.route('/agricultores/editar/<int:id_agricultor>', methods=['GET', 'POST'])
@permiso_de_admin('agricultores.editar')  # Permiso: editar agricultor
def editar_agricultor(id_agricultor):
    agricultor = obtener_agricultor(id_agricultor)
    if not agricultor:
        flash("❌ Agricultor no encontrado.", "danger")
        return redirect(url_for('agricultores.index'))

    if request.method == 'POST':
        datos = {
            'id_agricultor': id_agricultor,
            'codigo_agricultor': request.form['codigo_agricultor'].strip(),
            'dni': request.form['dni'].strip(),
            'nombres': request.form['nombres'].strip(),
            'apellidos': request.form['apellidos'].strip(),
            'telefono': request.form['telefono'].strip(),
            'direccion': request.form['direccion'].strip(),
            'correo': request.form['correo'].strip(),
            'zona': request.form['zona'].strip(),
            'cultivo_principal': request.form['cultivo_principal'].strip(),
            'estado': int(request.form.get('estado', 1))  # 1 = Activo, 0 = Inactivo
        }
        try:
            actualizar_agricultor(datos)
            flash("✅ Agricultor actualizado correctamente.", "success")
            return redirect(url_for('agricultores.index'))
        except ValueError as e:
            flash(str(e), "danger")

    return render_template('agricultores/form.html', agricultor=agricultor)

# ==============================
# 📌 Desactivar Agricultor
# ==============================
@agricultores_bp.route('/agricultores/desactivar/<int:id_agricultor>')
@permiso_de_admin('agricultores.estado')
def desactivar_agricultor_route(id_agricultor):
    desactivar_agricultor(id_agricultor)
    flash("🛑 Agricultor desactivado correctamente.", "warning")
    return redirect(url_for('agricultores.index'))

# ==============================
# 📌 Activar Agricultor
# ==============================
@agricultores_bp.route('/agricultores/activar/<int:id_agricultor>')
@permiso_de_admin('agricultores.estado')
def activar_agricultor_route(id_agricultor):
    activar_agricultor(id_agricultor)
    flash("✅ Agricultor activado correctamente.", "success")
    return redirect(url_for('agricultores.index'))

# ==============================
# 📌 Detalle de Agricultor
# ==============================
@agricultores_bp.route('/agricultores/<int:id_agricultor>')
@permiso_de_admin('agricultores.detalles')  # Permiso: ver detalle agricultor
def detalle_agricultor(id_agricultor):
    agricultor = obtener_agricultor(id_agricultor)
    if not agricultor:
        flash("❌ Agricultor no encontrado.", "danger")
        return redirect(url_for('agricultores.index'))
    
    return render_template('agricultores/detalle.html', agricultor=agricultor)

# ==============================
# 📦 Entregables de un agricultor
# ==============================
@agricultores_bp.route('/agricultores/<int:id_agricultor>/entregables')
@permiso_de_admin('agricultores.entregables')  # o crea un permiso específico
def entregables_agricultor(id_agricultor):
    agricultor = obtener_agricultor(id_agricultor)
    if not agricultor:
        flash("❌ Agricultor no encontrado.", "danger")
        return redirect(url_for('agricultores.index'))

    entregables = obtener_entregables_por_agricultor(id_agricultor)
    return render_template('agricultores/entregables.html',
                           agricultor=agricultor,
                           entregables=entregables)