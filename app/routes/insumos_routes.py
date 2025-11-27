from flask import Blueprint, flash, jsonify, render_template, redirect, request, url_for
from app.models.insumos_model import (
    listar_insumos, agregar_insumo, cambiar_estado, listar_insumos_con_filtros, obtener_insumo, actualizar_insumo
)
from app.models.categorias_model import listar_categorias
from app.models.variedades_model import listar_variedades
from app.utils.auth import permiso_de_admin  # 🔹 Para proteger ciertas rutas

insumos_bp = Blueprint('insumos', __name__)

# ==============================
# LISTAR INSUMOS
# ==============================
@insumos_bp.route('/insumos')
@permiso_de_admin('insumos.ver') # Ver insumos
def index():
    insumos = listar_insumos()
    return render_template('insumos/index.html', insumos=insumos)

# ==============================
# CREAR NUEVO INSUMO
# ==============================
@insumos_bp.route('/insumos/nuevo', methods=['GET', 'POST'])
@permiso_de_admin('insumos.crear') # Nuevo Insumo
def nuevo_insumo():
    if request.method == 'POST':
        datos = {
            'codigo_insumo': request.form['codigo_insumo'],
            'nombre_insumo': request.form['nombre_insumo'],
            'id_categoria': int(request.form['id_categoria']),
            'id_variedad': int(request.form['id_variedad']) if request.form.get('id_variedad') else None,
            'stock_actual': float(request.form['stock_actual']),
            'unidad_medida': request.form['unidad_medida'],
            'fecha_vencimiento': request.form['fecha_vencimiento'] or None,
            'descripcion': request.form['descripcion'],
            'estado': True
        }
        try:
            agregar_insumo(datos)
            flash("✅ Insumo agregado correctamente", "success")
            return redirect(url_for('insumos.index'))
        except ValueError as e:
            flash(str(e), "danger")

    categorias = listar_categorias()
    variedades = listar_variedades()
    return render_template('insumos/form.html', categorias=categorias, variedades=variedades, insumo=None)

# ==============================
# EDITAR INSUMO
# ==============================
@insumos_bp.route('/insumos/editar/<int:id_insumo>', methods=['GET', 'POST'])
@permiso_de_admin('insumos.editar')  # Editar insumo
def editar_insumo(id_insumo):
    insumo = obtener_insumo(id_insumo)
    if not insumo:
        flash("⚠️ Insumo no encontrado", "warning")
        return redirect(url_for('insumos.index'))

    if request.method == 'POST':
        datos = {
            'id_insumo': id_insumo,
            'codigo_insumo': request.form['codigo_insumo'],
            'nombre_insumo': request.form['nombre_insumo'],
            'id_categoria': int(request.form['id_categoria']),
            'id_variedad': int(request.form['id_variedad']) if request.form.get('id_variedad') else None,
            'stock_actual': float(request.form['stock_actual']),
            'unidad_medida': request.form['unidad_medida'],
            'fecha_vencimiento': request.form['fecha_vencimiento'] or None,
            'descripcion': request.form['descripcion']
        }
        try:
            actualizar_insumo(datos)
            flash("✅ Insumo actualizado correctamente", "success")
            return redirect(url_for('insumos.index'))
        except ValueError as e:
            flash(str(e), "danger")

    categorias = listar_categorias()
    variedades = listar_variedades()
    return render_template('insumos/form.html', categorias=categorias, variedades=variedades, insumo=insumo)

# ==============================
# CAMBIAR ESTADO (DESACTIVAR / ACTIVAR)
# ==============================
@insumos_bp.route('/insumos/desactivar/<int:id_insumo>')
@permiso_de_admin('insumos.desactivar') # cambiar estado 
def desactivar_insumo(id_insumo):
    cambiar_estado(id_insumo, False)
    flash("⚠️ Insumo desactivado", "warning")
    return redirect(url_for('insumos.index'))

@insumos_bp.route('/insumos/activar/<int:id_insumo>')
@permiso_de_admin('insumos.activar')
def activar_insumo(id_insumo):
    cambiar_estado(id_insumo, True)
    flash("✅ Insumo activado", "success")
    return redirect(url_for('insumos.index'))


@insumos_bp.route('/insumos/buscar_insumo', methods=['GET'])
def buscar_insumo():
    q = request.args.get("q", "").strip()
    insumos = listar_insumos_con_filtros(q)
    return render_template('insumos/_tabla_insumos.html', insumos=insumos)

@insumos_bp.route('/insumos/buscar_categoria')
def buscar_categoria():
    q = request.args.get("q", "").strip().lower()
    categorias = listar_categorias()

    if q:
        categorias = [
            c for c in categorias
            if q in (c.get("nombre_categoria") or "").lower()
            or q in (c.get("codigo_categoria") or "").lower()
        ]

    data = [
        {
            "id": c["id_categoria"],
            "text": f"🏷️ {c['codigo_categoria']} - {c['nombre_categoria']}"
        }
        for c in categorias
    ]
    return jsonify(data)


@insumos_bp.route('/insumos/buscar_variedades')
def buscar_variedades():
    id_categoria = request.args.get('id_categoria', type=int)
    q = request.args.get("q", "").strip().lower()
    variedades = listar_variedades(id_categoria=id_categoria)

    if id_categoria:
        variedades = [v for v in variedades if v.get('id_categoria') == id_categoria]

    if q:
        variedades = [
            v for v in variedades
            if q in (v.get("nombre_variedad") or "").lower()
            or q in (v.get("codigo_variedad") or "").lower()
        ]
    data = [
        {"id": v["id_variedad"], "text": f"🌱 {v['nombre_variedad']}"}
        for v in variedades
    ]

    return jsonify(data)