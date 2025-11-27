import json
from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash, session
from app.helpers import get_usuario_actual
from app.models.movimientos_model import (
    actualizar_nota_movimiento, aprobar_nota_movimiento, crear_nota_movimiento, agregar_detalle_movimiento, eliminar_detalles_movimiento,
    listar_notas_movimiento, actualizar_estado_nota, listar_origenes,
    listar_salidas_jabas, obtener_detalles_por_nota, obtener_nota_completa, obtener_nota_por_id, registrar_devolucion_jabas,
    kardex_insumo
)
from app.models.insumos_model import listar_insumos, obtener_insumo
from app.models.tipo_movimiento_model import listar_tipos_movimiento
from app.models.agricultores_model import listar_agricultores  # opcional, legacy
from app.utils.auth import permiso_de_admin
from datetime import date, datetime
from mysql.connector import Error as MySQLError

movimientos_bp = Blueprint('movimientos', __name__)


# ==============================
# 📌 Listado de movimientos
# ==============================
@movimientos_bp.route('/movimientos')
@permiso_de_admin('movimientos.ver')
def index():
    movimientos = listar_notas_movimiento()
    return render_template('movimientos/index.html', movimientos=movimientos)


# ==============================
# 📌 Registrar nueva nota + detalles
# ==============================
@movimientos_bp.route('/movimientos/nuevo', methods=['GET', 'POST'])
@permiso_de_admin('movimientos.crear')
def nuevo_movimiento():
    if request.method == 'POST':
        try:
            # lectura segura del JSON de detalles
            detalles_raw = request.form.get('detalles')
            if not detalles_raw:
                raise ValueError("No se recibieron detalles. Agrega al menos un insumo.")

            try:
                detalles = json.loads(detalles_raw)
            except Exception:
                raise ValueError("Detalles inválidos (JSON).")

            if not isinstance(detalles, list) or len(detalles) == 0:
                raise ValueError("La lista de detalles está vacía.")

            # obtener id_usuario desde sesión (más seguro)
            id_usuario = get_usuario_actual()
            if not id_usuario:
                raise ValueError("Usuario no identificado en sesión.")

            # validar campos obligatorios de cabecera
            if not request.form.get('id_tipo'):
                raise ValueError("Selecciona un tipo de movimiento.")
            if not request.form.get('id_origen'):
                raise ValueError("Selecciona el origen/destino.")

            id_tipo = int(request.form['id_tipo'])
            id_origen = int(request.form['id_origen'])
            referencia = request.form.get('referencia') or None
            observacion = request.form.get('observacion') or None

            # 1️⃣ Crear nota (SP)
            resultado = crear_nota_movimiento(
                id_tipo=id_tipo,
                referencia=referencia,
                id_usuario=int(id_usuario),
                id_origen=id_origen,
                observacion=observacion
            )

            # resultado debe contener id_nota (según SP)
            id_nota = resultado.get('id_nota') if isinstance(resultado, dict) else None
            if not id_nota:
                # algunos SP retornan directamente el recordset, intentamos extraer
                try:
                    id_nota = int(resultado)
                except Exception:
                    raise ValueError("No se pudo obtener el id de la nota creada.")

            # 2️⃣ Insertar detalles (SP por cada fila)
            for det in detalles:
                # validaciones mínimas por seguridad
                if not det.get('id_insumo') or det.get('cantidad') in (None, "", 0):
                    raise ValueError("Cada detalle debe tener id_insumo y cantidad válidos.")
                agregar_detalle_movimiento(
                    id_nota=id_nota,
                    id_insumo=int(det['id_insumo']),
                    id_tipo=id_tipo,
                    cantidad=float(det['cantidad']),
                    unidad_medida=str(det.get('unidad_medida') or '')
                )

            flash(f"✅ Nota registrada correctamente (ID: {id_nota})", "success")
            return redirect(url_for('movimientos.index'))

        except MySQLError as db_err:
            # Errores de BD
            flash(f"❌ Error de base de datos: {db_err}", "danger")
            return redirect(url_for('movimientos.nuevo_movimiento'))
        except Exception as e:
            flash(f"❌ Error al registrar movimiento: {e}", "danger")
            return redirect(url_for('movimientos.nuevo_movimiento'))

    # GET → cargar combos (Select2 usará AJAX para orígenes/insumos)
    insumos = listar_insumos()
    tipos_movimiento = listar_tipos_movimiento()
    origenes = listar_origenes()  

    return render_template(
        'movimientos/registrar.html',
        insumos=insumos,
        tipos_movimiento=tipos_movimiento,
        origenes=origenes,
        today=date.today().isoformat()
    )

# ==============================
# 📌 Editar cabecera + detalles de la nota
# ==============================
@movimientos_bp.route('/movimientos/actualizar/<int:id_nota>', methods=['GET', 'POST'])
@permiso_de_admin('movimientos.editar')
def actualizar_nota_movimiento_route(id_nota):
    if request.method == 'POST':
        try:
            detalles_raw = request.form.get('detalles')
            if not detalles_raw:
                raise ValueError("No se recibieron detalles.")
            detalles = json.loads(detalles_raw)

            id_usuario = get_usuario_actual()
            if not id_usuario:
                raise ValueError("Usuario no identificado en sesión.")

            id_tipo = int(request.form['id_tipo'])
            id_origen = int(request.form['id_origen'])
            referencia = request.form.get('referencia') or None
            observacion = request.form.get('observacion') or None
            fecha = request.form.get('fecha') or date.today().isoformat()

            # 🔹 Actualizar cabecera
            actualizar_nota_movimiento(
                id_nota=id_nota,
                id_tipo=id_tipo,
                referencia=referencia,
                id_usuario=id_usuario,
                id_origen=id_origen,
                observacion=observacion,
                fecha=fecha
            )

            # 🔹 Reemplazar detalles
            eliminar_detalles_movimiento(id_nota)
            for det in detalles:
                agregar_detalle_movimiento(
                    id_nota=id_nota,
                    id_insumo=int(det['id_insumo']),
                    id_tipo=id_tipo,
                    cantidad=float(det['cantidad']),
                    unidad_medida=str(det.get('unidad_medida') or '')
                )

            flash(f"✅ Nota actualizada correctamente (ID: {id_nota})", "success")
            return redirect(url_for('movimientos.index'))

        except Exception as e:
            flash(f"❌ Error al actualizar movimiento: {e}", "danger")
            return redirect(url_for('movimientos.actualizar_nota_movimiento_route', id_nota=id_nota))

    # GET → cargar datos
    movimiento = obtener_nota_por_id(id_nota)
    detalles = obtener_detalles_por_nota(id_nota)
    tipos_movimiento = listar_tipos_movimiento()
    origenes = listar_origenes()

    return render_template(
        'movimientos/editar.html',
        movimiento=movimiento,
        detalles=detalles,
        tipos_movimiento=tipos_movimiento,
        origenes=origenes
    )

# ==============================
# 📌 Actualizar estado de nota (usado por modal en index)
# ==============================
@movimientos_bp.route('/movimientos/actualizar_estado/<int:id_nota>', methods=['POST'])
@permiso_de_admin('movimientos.editar')
def actualizar_estado_nota_movimiento(id_nota):
    try:
        nuevo_estado = request.form.get('estado')
        if nuevo_estado not in ('pendiente', 'aprobado', 'anulado'):
            raise ValueError("Estado inválido.")

        # Obtener el estado actual de la nota
        nota = obtener_nota_por_id(id_nota)
        if not nota:
            raise ValueError("Nota no encontrada.")

        estado_actual = nota["estado"]

        # 🔒 Lógica de transición de estados
        if estado_actual == "aprobado":
            raise ValueError("Una nota aprobada no puede ser modificada ni anulada.")

        if estado_actual == "anulado":
            raise ValueError("Una nota anulada no puede cambiar de estado.")

        if estado_actual == "pendiente" and nuevo_estado == "aprobado":
            aprobar_nota_movimiento(id_nota)   # 🔹 actualiza stock
        elif estado_actual == "pendiente" and nuevo_estado == "anulado":
            actualizar_estado_nota(id_nota, nuevo_estado)
        elif estado_actual == "pendiente" and nuevo_estado == "pendiente":
            raise ValueError("La nota ya está en pendiente.")
        else:
            raise ValueError(f"No se puede cambiar de {estado_actual} a {nuevo_estado}.")

        flash(f"✅ Estado actualizado a {nuevo_estado}", "success")

    except Exception as e:
        flash(f"❌ Error al actualizar estado: {e}", "danger")

    return redirect(url_for('movimientos.index'))

# ==============================
# 📌 Kardex de un insumo
# ==============================
@movimientos_bp.route('/movimientos/kardex/<int:id_insumo>')
@permiso_de_admin('movimientos.kardex')
def kardex(id_insumo):
    movimientos = kardex_insumo(id_insumo)
    insumo = obtener_insumo(id_insumo)
    return render_template(
        'movimientos/kardex.html',
        movimientos=movimientos,
        id_insumo=id_insumo,
        nombre_insumo=insumo["nombre_insumo"] if insumo else "Desconocido"
    )

# ==============================
# 📌 ver detalle movimiento
# ==============================
@movimientos_bp.route('/movimientos/<int:id_nota>/detalle')
@permiso_de_admin('movimientos.ver')
def ver_detalle(id_nota):
    cabecera, detalles = obtener_nota_completa(id_nota)
    if not cabecera:
        flash("⚠️ Nota no encontrada.", "warning")
        return redirect(url_for('movimientos.index'))
    return render_template('movimientos/detalle.html', cabecera=cabecera, detalles=detalles)

@movimientos_bp.route('/movimientos/<int:id_nota>/reporte')
@permiso_de_admin('movimientos.ver')
def reporte_movimiento(id_nota):
    cabecera, detalles = obtener_nota_completa(id_nota)
    if not cabecera:
        flash("⚠️ Nota no encontrada.", "warning")
        return redirect(url_for('movimientos.index'))
    return render_template('movimientos/Nota_Movimiento_individual.html', cabecera=cabecera, detalles=detalles, now=datetime.now())

# ==============================
# 📌 Control de jabas: listar salidas (recibe id_agricultor aún)
# ==============================
@movimientos_bp.route('/movimientos/salidas_jabas/<int:id_agricultor>')
def salidas_jabas(id_agricultor):
    salidas = listar_salidas_jabas(id_agricultor)
    return jsonify(salidas)


# ==============================
# 📌 Control de jabas: registrar devolución
# ==============================
@movimientos_bp.route('/movimientos/devolucion_jabas', methods=['POST'])
def devolucion_jabas():
    try:
        id_recepcion = int(request.form['id_recepcion'])
        id_agricultor = int(request.form['id_agricultor'])
        cantidad_devuelta = int(request.form['cantidad_devuelta'])

        registrar_devolucion_jabas(id_recepcion, id_agricultor, cantidad_devuelta)

        flash("✅ Devolución de jabas registrada correctamente.", "success")
    except Exception as e:
        flash(f"❌ Error al registrar devolución: {e}", "danger")

    return redirect(url_for('movimientos.index'))


# ==============================
# 📌 Endpoints para Select2 / AJAX
# ==============================
@movimientos_bp.route('/movimientos/buscar_insumos')
def buscar_insumos():
    q = request.args.get("q", "").strip().lower()
    insumos = listar_insumos()
    if q:
        insumos = [i for i in insumos if q in (i.get("nombre_insumo") or "").lower()]
    data = [{"id": i["id_insumo"], "text": i["nombre_insumo"]} for i in insumos]
    return jsonify(data)


@movimientos_bp.route('/movimientos/buscar_agricultores')
def buscar_agricultores():
    # legacy: si alguna vista todavía usa este endpoint
    q = request.args.get("q", "").strip().lower()
    agricultores = listar_agricultores()
    if q:
        agricultores = [a for a in agricultores if q in (a.get("nombre_completo") or "").lower()]
    data = [{"id": a["id_agricultor"], "text": a["nombre_completo"]} for a in agricultores]
    return jsonify(data)


@movimientos_bp.route('/movimientos/buscar_origenes')
def buscar_origenes():
    q = request.args.get("q", "").lower()
    origenes = listar_origenes()  # 🔹 agricultores + almacenes

    if q:
        origenes = [
            o for o in origenes
            if q in (o["nombre"] or "").lower()
            or q in (o.get("dni") or "").lower()
            or q in (o.get("codigo") or "").lower()
        ]

    data = [
        {
            "id": o["id_origen"],
            "text": (
                ("🏢 " if o["tipo"] == "almacen" else "👨‍🌾 ")
                + o["nombre"]
                + (f" - DNI: {o['dni']}" if o.get("dni") else "")
                + (f" ({o['codigo']})" if o.get("codigo") else "")
            )
        }
        for o in origenes
    ]
    return jsonify(data)

@movimientos_bp.route('/movimientos/buscar', methods=['GET'])
@permiso_de_admin('movimientos.ver')
def buscar_movimiento():
    q = request.args.get("q", "").strip()
    movimientos = listar_notas_movimiento(q, None, None, None, None)
    return render_template('movimientos/_tabla_movimientos.html', movimientos=movimientos)
