import json
from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash
from datetime import date, datetime
from mysql.connector import Error as MySQLError

from app.helpers import buscar_agricultores_json, get_usuario_actual
from app.models import get_db_connection
from app.utils.auth import permiso_de_admin

# === MODELOS ===
from app.models.recepcion_model import (
    actualizar_detalle_recepcion, eliminar_detalle_recepcion, listar_recepciones, crear_recepcion, agregar_detalle_recepcion,
    actualizar_recepcion, eliminar_detalles_recepcion, obtener_notas_salida, obtener_recepcion_completa, obtener_recepcion_por_id, obtener_detalles_recepcion,
    aprobar_recepcion, actualizar_estado_recepcion
)
from app.models.agricultores_model import listar_agricultores
from app.models.variedades_model import listar_variedades
from app.models.usuarios_model import listar_usuarios

# =======================================
# 📦 Blueprint de Recepciones
# =======================================
recepcion_bp = Blueprint('recepcion', __name__, url_prefix='/recepcion')


# ==============================
# 📋 Listado de recepciones
# ==============================
@recepcion_bp.route('/recepciones')
@permiso_de_admin('recepcion.ver')
def index():
    recepciones = listar_recepciones()
    return render_template('recepcion/index.html', recepciones=recepciones)


# ==============================
# ➕ Nueva recepción
# ==============================
@recepcion_bp.route('/recepciones/nueva', methods=['GET', 'POST'])
@permiso_de_admin('recepcion.crear')
def nueva_recepcion():
    if request.method == 'POST':
        try:
            # detalles vienen como JSON en input hidden "detalles"
            detalles_raw = request.form.get('detalles')
            if not detalles_raw:
                raise ValueError("No se recibieron detalles de recepción.")
            try:
                detalles = json.loads(detalles_raw)
            except Exception:
                raise ValueError("Detalles inválidos (JSON no válido).")
            if not isinstance(detalles, list) or len(detalles) == 0:
                raise ValueError("Debes agregar al menos un detalle.")

            # usuario actual (id de responsable) → get_usuario_actual puede devolver id o dict
            id_responsable = get_usuario_actual()
            if not id_responsable:
                raise ValueError("Usuario no identificado en sesión.")

            # campos cabecera
            id_agricultor = request.form.get('id_agricultor')
            id_nota_salida = request.form.get('id_nota_salida') or None
            fecha_recepcion = request.form.get('fecha_recepcion') or None  # si no viene, el SP puede tomar NOW()
            observaciones = request.form.get('observaciones') or None

            if not id_agricultor:
                raise ValueError("Falta el agricultor.")
            # nota de salida puede ser opcional (None) según tu lógica; aquí la validamos si la UI la requiere:
            if not id_nota_salida:
                raise ValueError("Debes seleccionar una nota de salida.")

            # 4) crear recepción (cabecera)
            resultado = crear_recepcion(
                id_nota_salida=int(id_nota_salida) if id_nota_salida else None,
                id_agricultor=int(id_agricultor),
                fecha_recepcion=fecha_recepcion,
                observaciones=observaciones,
                id_responsable=int(id_responsable)
            )

            # Compatibilidad: resultado puede ser dict o int (aunque el model ahora devuelve dict)
            if isinstance(resultado, dict):
                id_recepcion = resultado.get('id_recepcion')
            else:
                id_recepcion = int(resultado)

            if not id_recepcion:
                raise ValueError("No se pudo obtener el ID de la recepción creada.")

            # 5) Insertar detalles -> llamar al model agregar_detalle_recepcion con la estructura correcta
            for det in detalles:
                try:
                    peso_bruto = float(det.get('peso_bruto') or 0)
                    cantidad_jabas = int(det.get('cantidad_jabas') or 0)
                    peso_neto = peso_bruto - (cantidad_jabas * 2)  # cálculo automático

                    agregar_detalle_recepcion(
                        id_recepcion=int(id_recepcion),
                        id_variedad=int(det['id_variedad']),
                        lote=str(det.get('lote') or ''),
                        peso_bruto=peso_bruto,
                        cantidad_jabas=cantidad_jabas,
                        peso_neto=peso_neto,
                        unidad_medida=str(det.get('unidad') or 'kg')
                    )
                except Exception as e:
                    raise ValueError(f"Error al agregar detalle: {e}")

            flash(f"✅ Recepción registrada correctamente (ID: {id_recepcion})", "success")
            return redirect(url_for('recepcion.index'))

        except MySQLError as db_err:
            flash(f"❌ Error de base de datos: {db_err}", "danger")
        except Exception as e:
            flash(f"❌ Error al registrar recepción: {e}", "danger")

        return redirect(url_for('recepcion.nueva_recepcion'))

    # GET → cargar combos
    agricultores = listar_agricultores()
    variedades = listar_variedades('MP') 
    usuario_actual = get_usuario_actual()

    return render_template(
        'recepcion/registrar.html',
        agricultores=agricultores,
        variedades=variedades,
        usuario_actual=usuario_actual,
        today=date.today().isoformat()
    )

# ==============================
# ✏️ Editar recepción
# ==============================
@recepcion_bp.route('/recepciones/editar/<int:id_recepcion>', methods=['GET', 'POST'])
@permiso_de_admin('recepcion.editar')
def editar_recepcion(id_recepcion):
    if request.method == 'POST':
        try:
            detalles_raw = request.form.get('detalles')
            if not detalles_raw:
                raise ValueError("No se recibieron detalles.")

            detalles = json.loads(detalles_raw)
            
            id_responsable = get_usuario_actual()
            if not id_responsable:
                raise ValueError("Usuario no identificado en sesión.")

            id_agricultor = int(request.form['id_agricultor'])
            observaciones = request.form.get('observacion') or None      

            # 🔹 Actualizar cabecera
            actualizar_recepcion(
                id_recepcion=id_recepcion,
                id_agricultor=id_agricultor,
                id_responsable=id_responsable,
                observaciones=observaciones,
                estado='pendiente'
            )

            # 🔹 Anular todos los detalles anteriores
            eliminar_detalles_recepcion(id_recepcion)

            # 🔹 Insertar, actualiza y anula todos los detalles del form
            for det in detalles:
                peso_bruto = float(det['peso_bruto'])
                cantidad_jabas = int(det['cantidad_jabas'])
                peso_neto = peso_bruto - (cantidad_jabas * 2)

                if det['estado'] == 'nuevo':
                    agregar_detalle_recepcion(
                        id_recepcion=id_recepcion,
                        id_variedad=det['id_variedad'],
                        lote=det['lote'],
                        peso_bruto=peso_bruto,
                        cantidad_jabas=cantidad_jabas,
                        peso_neto=peso_neto,
                        unidad_medida=det.get('unidad_medida', 'kg')
                    )
                elif det['estado'] == 'modificado':
                    actualizar_detalle_recepcion(
                        id_detalle=int(det['id_detalle']),
                        id_variedad=det['id_variedad'],
                        lote=det['lote'],
                        peso_bruto=peso_bruto,
                        cantidad_jabas=cantidad_jabas,
                        peso_neto=peso_neto,
                        unidad_medida=det.get('unidad_medida', 'kg')
                    )
                elif det['estado'] == 'eliminado':
                    eliminar_detalle_recepcion(int(det['id_detalle']))

            flash("✅ Recepción actualizada correctamente.", "success")
            return redirect(url_for('recepcion.index'))

        except Exception as e:
            flash(f"❌ Error al actualizar recepción: {e}", "danger")
            return redirect(url_for('recepcion.editar_recepcion', id_recepcion=id_recepcion))

    # GET → cargar datos
    recepcion = obtener_recepcion_por_id(id_recepcion)
    detalles = obtener_detalles_recepcion(id_recepcion)
    agricultores = listar_agricultores()
    variedades = listar_variedades('MP')
    responsables = listar_usuarios()
    
    return render_template(
        'recepcion/editar.html',
        recepcion=recepcion,
        detalles=detalles,
        agricultores=agricultores,
        variedades=variedades,
        responsables=responsables
    )


# ==============================
# 👁️ Ver detalle
# ==============================
@recepcion_bp.route('/recepciones/<int:id_recepcion>/detalle')
@permiso_de_admin('recepcion.ver')
def ver_detalle_recepcion(id_recepcion):
    cabecera, detalles = obtener_recepcion_completa(id_recepcion)

    if not cabecera:
        flash("⚠️ Recepción no encontrada.", "warning")
        return redirect(url_for('recepcion.index'))

    return render_template(
        'recepcion/detalle.html',
        cabecera=cabecera,
        detalles=detalles
    )

@recepcion_bp.route('/recepciones/<int:id_recepcion>/reporte')
@permiso_de_admin('recepcion.ver')
def reporte_recepcion(id_recepcion):
    cabecera, detalles = obtener_recepcion_completa(id_recepcion)

    if not cabecera:
        flash("⚠️ Recepción no encontrada.", "warning")
        return redirect(url_for('recepcion.index'))

    return render_template(
        'recepcion/reporte_Recepcion_Individual.html',
        cabecera=cabecera,
        detalles=detalles,
        now=datetime.now()
    )

@recepcion_bp.route('/recepcion/anular/<int:id_recepcion>', methods=['POST'])
@permiso_de_admin('recepcion.eliminar')
def anular_recepcion(id_recepcion):
    try:
        # 1️⃣ Marcar detalles como anulados
        eliminar_detalles_recepcion(id_recepcion)

        # 2️⃣ Marcar cabecera como anulada
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE recepcion_materia_prima SET estado='anulado' WHERE id_recepcion=%s",
            (id_recepcion,)
        )
        conn.commit()
        flash(f"✅ Recepción {id_recepcion} anulada correctamente.", "success")
    except Exception as e:
        conn.rollback()
        flash(f"❌ Error al anular la recepción: {e}", "danger")
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('recepcion.index'))


# ==============================
# 🔄 Actualizar estado (pendiente/aprobado/anulado)
# ==============================
@recepcion_bp.route('/actualizar_estado/<int:id_recepcion>', methods=['POST'])
@permiso_de_admin('recepcion.editar')
def actualizar_estado(id_recepcion):
    try:
        nuevo_estado = request.form.get('estado')
        if nuevo_estado not in ('pendiente', 'aprobado', 'anulado'):
            raise ValueError("Estado inválido.")

        recepcion = obtener_recepcion_por_id(id_recepcion)
        if not recepcion:
            raise ValueError("Recepción no encontrada.")

        estado_actual = recepcion["estado"]

        if estado_actual == "aprobado":
            raise ValueError("Una recepción aprobada no puede modificarse.")
        if estado_actual == "anulado":
            raise ValueError("Una recepción anulada no puede modificarse.")

        if estado_actual == "pendiente" and nuevo_estado == "aprobado":
            aprobar_recepcion(id_recepcion)
        elif estado_actual == "pendiente" and nuevo_estado == "anulado":
            actualizar_estado_recepcion(id_recepcion, nuevo_estado)
        elif estado_actual == "pendiente" and nuevo_estado == "pendiente":
            raise ValueError("La recepción ya está pendiente.")
        else:
            raise ValueError(f"No se puede cambiar de {estado_actual} a {nuevo_estado}.")

        flash(f"✅ Estado actualizado a {nuevo_estado}", "success")

    except Exception as e:
        flash(f"❌ Error al actualizar estado: {e}", "danger")

    return redirect(url_for('recepcion.index'))


# ==============================
# 🔍 Endpoints AJAX para Select2
# ==============================
@recepcion_bp.route('/buscar_agricultor')
def buscar_agricultores_recepcion():
     return buscar_agricultores_json()

@recepcion_bp.route('/buscar_variedades')
def buscar_variedades_recepcion():
    q = request.args.get("q", "").strip().lower()

    # 🔹 Solo variedades de Materia Prima (código 'MP')
    variedades = listar_variedades(None, 'MP')
    print("📦 VARIEDADES MP:", variedades)

    # 🔹 Si se está buscando algo, filtrar por nombre
    if q:
        variedades = [v for v in variedades if q in (v.get("nombre_variedad") or "").lower()]

    # 🔹 Estructura esperada por Select2
    data = [{"id": v["id_variedad"], "text": v["nombre_variedad"]} for v in variedades]
    return jsonify(data)


@recepcion_bp.route('/recepciones/buscar_responsables')
def buscar_responsables_recepcion():
    q = request.args.get("q", "").strip().lower()
    responsables = listar_usuarios()
    if q:
        responsables = [r for r in responsables if q in (r.get("nombre_completo") or "").lower()]
    data = [{"id": r["id_responsable"], "text": r["nombre_completo"]} for r in responsables]
    return jsonify(data)

@recepcion_bp.route('/get_notas_salida/<int:id_agricultor>', methods=['GET'])
def get_notas_salida(id_agricultor):
    notas = obtener_notas_salida(id_agricultor)
    return jsonify(notas)

@recepcion_bp.route('/buscar', methods=['GET'])
@permiso_de_admin('recepcion.ver')
def buscar_recepcion():
    q = request.args.get("q", "").strip()
    recepciones = listar_recepciones(
        p_q=q, p_id_agricultor=None, p_estado=None, p_fecha_inicio=None, p_fecha_fin=None
    )
    return render_template('recepcion/_tabla_recepciones.html', recepciones=recepciones)
