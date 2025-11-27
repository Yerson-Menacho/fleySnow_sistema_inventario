from flask import Blueprint, render_template, redirect, request, url_for, flash
from app.models.categorias_model import (
    actualizar_categoria, eliminar_categoria, listar_categorias,
    agregar_categoria, obtener_categoria
)
from app.utils.auth import permiso_de_admin  # 🔹 Restricción para admins

categorias_bp = Blueprint('categorias', __name__)

# ==============================
# 📌 Listado de categorías
# ==============================
@categorias_bp.route('/categorias')
@permiso_de_admin('categoria.ver') #gestionar categoria
def index():
    categorias = listar_categorias()
    return render_template('categorias/index.html', categorias=categorias)

# ==============================
# 📌 Nueva categoría
# ==============================
@categorias_bp.route('/categorias/nueva', methods=['GET', 'POST'])
@permiso_de_admin('insumos.cat_crear') #Nueva Categoria
def nueva_categoria():
    if request.method == 'POST':
        datos = {
            'codigo_categoria': request.form['codigo_categoria'].strip(),
            'nombre_categoria': request.form['nombre_categoria'].strip()
        }
        try:
            agregar_categoria(datos)
            flash("✅ Categoría agregada correctamente.", "success")
            return redirect(url_for('categorias.index'))
        except ValueError as e:
            flash(str(e), "danger")
            return render_template('categorias/form.html', categoria=None)

    return render_template('categorias/form.html', categoria=None)

# ==============================
# 📌 Editar categoría
# ==============================
@categorias_bp.route('/categorias/editar/<int:id_categoria>', methods=['GET', 'POST'])
@permiso_de_admin('insumos.cat_editar') # Editar categoria
def editar_categoria(id_categoria):
    categoria = obtener_categoria(id_categoria)
    if not categoria:
        flash("⚠️ Categoría no encontrada.", "warning")
        return redirect(url_for('categorias.index'))

    if request.method == 'POST':
        datos = {
            'id_categoria': id_categoria,
            'codigo_categoria': request.form['codigo_categoria'].strip(),
            'nombre_categoria': request.form['nombre_categoria'].strip()
        }
        try:
            actualizar_categoria(datos)
            flash("✅ Categoría actualizada correctamente.", "success")
            return redirect(url_for('categorias.index'))
        except ValueError as e:
            flash(str(e), "danger")
            return render_template('categorias/form.html', categoria=categoria)

    return render_template('categorias/form.html', categoria=categoria)

# ==============================
# 📌 Eliminar categoría
# ==============================
@categorias_bp.route('/categorias/eliminar/<int:id_categoria>', methods=['POST'])
@permiso_de_admin('insumos.cat_eliminar') # Eliminar categoria
def eliminar_categoria_route(id_categoria):
    try:
        eliminar_categoria(id_categoria)
        flash("🗑️ Categoría eliminada correctamente.", "success")
    except ValueError as e:
        flash(str(e), "danger")
    return redirect(url_for('categorias.index'))

