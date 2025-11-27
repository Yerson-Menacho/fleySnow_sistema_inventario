from flask import Blueprint, flash, render_template, redirect, request, url_for
from app.models.variedades_model import (
    listar_variedades, agregar_variedad, actualizar_variedad,
    eliminar_variedad, obtener_variedad
)
from app.models.categorias_model import listar_categorias
from app.utils.auth import permiso_de_admin  # 🔹 Para restringir a admins

variedades_bp = Blueprint('variedades', __name__)

# ==============================
# LISTAR VARIEDADES
# ==============================
@variedades_bp.route('/variedades')
@permiso_de_admin('variedad.ver') # gestina la lista de variedd
def index():
    variedades = listar_variedades()
    return render_template('variedades/index.html', variedades=variedades)

# ==============================
# CREAR NUEVA VARIEDAD
# ==============================
@variedades_bp.route('/variedades/nueva', methods=['GET', 'POST'])
@permiso_de_admin('insumos.var_crear') # nueva variedad
def nueva_variedad():
    if request.method == 'POST':
        datos = {
            'codigo_variedad': request.form['codigo_variedad'],
            'nombre_variedad': request.form['nombre_variedad'],
            'id_categoria': int(request.form['id_categoria'])
        }
        try:
            agregar_variedad(datos)
            flash("✅ Variedad agregada correctamente.", "success")
            return redirect(url_for('variedades.index'))
        except ValueError as e:
            flash(str(e), "danger")  # Error si hay duplicado u otro problema

    categorias = listar_categorias()
    return render_template('variedades/form.html', variedad=None, categorias=categorias)

# ==============================
# EDITAR VARIEDAD
# ==============================
@variedades_bp.route('/variedades/editar/<int:id_variedad>', methods=['GET', 'POST'])
@permiso_de_admin('insumos.var_editar')
def editar_variedad(id_variedad):
    variedad = obtener_variedad(id_variedad)
    if not variedad:
        flash("⚠️ Variedad no encontrada", "warning")
        return redirect(url_for('variedades.index'))

    categorias = listar_categorias()
    if request.method == 'POST':
        datos = {
            'id_variedad': id_variedad,
            'codigo_variedad': request.form['codigo_variedad'],
            'nombre_variedad': request.form['nombre_variedad'],
            'id_categoria': int(request.form['id_categoria'])
        }
        try:
            actualizar_variedad(datos)
            flash("✅ Variedad actualizada correctamente.", "success")
            return redirect(url_for('variedades.index'))
        except ValueError as e:
            flash(str(e), "danger")

    return render_template('variedades/form.html', variedad=variedad, categorias=categorias)

# ==============================
# ELIMINAR VARIEDAD
# ==============================
@variedades_bp.route('/variedades/eliminar/<int:id_variedad>')
@permiso_de_admin('insumos.var_eliminar')
def eliminar_variedad_route(id_variedad):
    try:
        eliminar_variedad(id_variedad)
        flash("🗑️ Variedad eliminada correctamente.", "success")
    except ValueError as e:
        flash(str(e), "danger")

    return redirect(url_for('variedades.index'))
