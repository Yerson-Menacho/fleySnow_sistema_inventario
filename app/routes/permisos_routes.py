from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.permisos_model import listar_acciones, guardar_permisos_usuario, obtener_permisos_usuario
from app.models.usuarios_model import listar_usuarios, obtener_usuario_por_id
from app.utils.auth import permiso_de_admin

permisos_bp = Blueprint("permisos", __name__, url_prefix="/permisos")

# ✅ Listar usuarios para asignar permisos
@permisos_bp.route("/")
@permiso_de_admin('permisos.ver')
def index():
    usuarios = listar_usuarios()
    return render_template("usuarios/index.html", usuarios=usuarios)

# ✅ Gestionar permisos de un usuario
@permisos_bp.route("/gestionar/<int:id_usuario>", methods=["GET", "POST"])
@permiso_de_admin('permisos.asignar')
def gestionar(id_usuario):
    if request.method == "POST":
        seleccionados = request.form.getlist("acciones")  # valores serán códigos
        guardar_permisos_usuario(id_usuario, seleccionados)
        flash("✅ Permisos actualizados.", "success")
        return redirect(url_for("permisos.index"))

    # 🔹 Acciones disponibles, agrupadas por módulo
    acciones_por_modulo = listar_acciones()

    # 🔹 Permisos actuales del usuario
    permisos_actuales = obtener_permisos_usuario(id_usuario)
    permisos_codigos = [p["codigo"] for p in permisos_actuales if int(p.get("permitido", 0)) == 1]

    # 🔹 Obtener datos del usuario
    usuario = obtener_usuario_por_id(id_usuario)

    return render_template(
        "usuarios/permisos.html",
        acciones_por_modulo=acciones_por_modulo,
        permisos_codigos=permisos_codigos, 
        id_usuario=id_usuario,
        usuario=usuario
    )
