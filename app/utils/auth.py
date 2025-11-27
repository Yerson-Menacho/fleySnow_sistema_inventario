from flask import session, redirect, url_for, flash
from functools import wraps

ADMIN_ROLE_ID = 1

def es_admin():
    return session.get("id_rol") == ADMIN_ROLE_ID

def permiso_de_admin(codigo_accion=None):
    """Decorador que permite ejecutar la función si el usuario tiene el código de permiso"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # 👑 Admin → acceso total
            if es_admin():
                return f(*args, **kwargs)

            # 👤 Usuario normal → validar permisos por código
            permisos = session.get("permisos", [])
            if codigo_accion and codigo_accion not in permisos:
                flash("❌ No tienes permiso para acceder a esta acción.", "danger")
                return redirect(url_for("auth.home"))

            return f(*args, **kwargs)
        return decorated_function
    return decorator
