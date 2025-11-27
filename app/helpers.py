from flask import jsonify, request, session

from app.models.agricultores_model import listar_agricultores

def get_usuario_actual():
    """Devuelve el id del usuario logueado (None si no hay sesión activa)."""
    return session.get('id_usuario') or session.get('usuario_id')

def get_nombre_usuario():
    """Devuelve el nombre del usuario en sesión."""
    return session.get('nombre')

def get_rol_usuario():
    """Devuelve el rol actual del usuario en sesión."""
    return session.get('id_rol')

def get_permisos_usuario():
    """Devuelve la lista de permisos cargados en sesión."""
    return session.get('permisos', [])

def buscar_agricultores_json():
    """Busca agricultores según el texto ingresado y devuelve el resultado en formato JSON."""
    q = request.args.get("q", "").strip().lower()
    agricultores = listar_agricultores()

    if q:
        agricultores = [
            a for a in agricultores
            if q in (a.get("nombre_completo") or "").lower()
            or q in (a.get("codigo_agricultor") or "").lower()
            or q in (a.get("dni") or "").lower()
        ]

    data = [
        {
            "id": a["id_agricultor"],
            "text": f"👨‍🌾 {a['codigo_agricultor']} - {a['nombre_completo']} (DNI: {a['dni']})"
        }
        for a in agricultores
    ]

    return jsonify(data)