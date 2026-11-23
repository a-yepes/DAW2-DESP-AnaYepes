from functools import wraps

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from models import usuario

bp = Blueprint("auth", __name__)


def login_requerido(vista):
    """Decorador: si no hay sesión iniciada, manda al login en vez de mostrar la página."""
    @wraps(vista)
    def envoltorio(*args, **kwargs):
        if "usuario_id" not in session:
            flash("Inicia sesión para continuar.", "error")
            return redirect(url_for("auth.login"))
        return vista(*args, **kwargs)
    return envoltorio


def iniciar_sesion(u):
    """Guarda en la sesión los datos del usuario que acaba de entrar."""
    session.clear()
    session["usuario_id"] = u["id"]
    session["nombre"] = u["nombre"]
    session["es_admin"] = bool(u["es_admin"])


@bp.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nombre = request.form["nombre"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        # Validación en el servidor (aunque el HTML ya valide, nunca hay que fiarse del navegador)
        if len(nombre) < 2:
            flash("El nombre debe tener al menos 2 caracteres.", "error")
        elif "@" not in email:
            flash("El email no es válido.", "error")
        elif len(password) < 8:
            flash("La contraseña debe tener al menos 8 caracteres.", "error")
        elif usuario.buscar_por_email(email):
            flash("Ya existe una cuenta con ese email.", "error")
        else:
            usuario.crear(nombre, email, password)
            iniciar_sesion(usuario.buscar_por_email(email))
            flash(f"¡Bienvenida/o a TimeFlies, {nombre}!", "ok")
            return redirect(url_for("main.inicio"))

    return render_template("auth/registro.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]
        u = usuario.buscar_por_email(email)

        if usuario.password_correcta(u, password):
            iniciar_sesion(u)
            flash(f"¡Hola de nuevo, {u['nombre']}!", "ok")
            return redirect(url_for("main.inicio"))

        # Mismo mensaje si falla el email o la contraseña: no damos pistas a un atacante
        flash("Email o contraseña incorrectos.", "error")

    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    session.clear()
    flash("Has cerrado sesión. ¡Hasta el próximo viaje en el tiempo!", "ok")
    return redirect(url_for("main.inicio"))