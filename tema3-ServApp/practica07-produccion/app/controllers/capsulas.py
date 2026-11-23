from datetime import datetime

from flask import Blueprint, abort, flash, redirect, render_template, request, session, url_for

from controllers.auth import login_requerido
from models import capsula

bp = Blueprint("capsulas", __name__)


@bp.route("/capsulas")
@login_requerido
def lista():
    capsulas = capsula.de_usuario(session["usuario_id"])
    return render_template("capsulas/lista.html", capsulas=capsulas, emociones=capsula.EMOCIONES)


@bp.route("/capsulas/nueva", methods=["GET", "POST"])
@login_requerido
def nueva():
    if request.method == "POST":
        titulo = request.form["titulo"].strip()
        mensaje = request.form["mensaje"].strip()
        emocion = request.form.get("emocion", "ilusion")
        publica = 1 if request.form.get("publica") else 0

        # El campo datetime-local llega como texto: "2026-12-31T20:30"
        try:
            fecha = datetime.strptime(request.form["fecha_apertura"], "%Y-%m-%dT%H:%M")
        except ValueError:
            fecha = None

        if len(titulo) < 3:
            flash("El título debe tener al menos 3 caracteres.", "error")
        elif len(mensaje) < 10:
            flash("El mensaje debe tener al menos 10 caracteres.", "error")
        elif emocion not in capsula.EMOCIONES:
            flash("Elige una emoción de la lista.", "error")
        elif fecha is None or not capsula.es_fecha_futura(fecha):
            flash("La fecha de apertura tiene que estar en el futuro.", "error")
        else:
            capsula.crear(session["usuario_id"], titulo, mensaje, emocion, fecha, publica)
            flash(f"🔒 Cápsula sellada hasta el {fecha.strftime('%d/%m/%Y a las %H:%M')}.", "ok")
            return redirect(url_for("capsulas.lista"))

    return render_template("capsulas/nueva.html", emociones=capsula.EMOCIONES)


@bp.route("/capsulas/<int:capsula_id>")
@login_requerido
def ver(capsula_id):
    c = capsula.por_id(capsula_id, session["usuario_id"])
    if c is None:
        abort(404)   # no existe o no es tuya: respondemos "no encontrada"

    # Mientras esté sellada, el mensaje NO se envía a la plantilla (ni al navegador)
    if not c["abierta"]:
        c["mensaje"] = None

    return render_template("capsulas/ver.html", c=c, emociones=capsula.EMOCIONES)


@bp.route("/capsulas/<int:capsula_id>/abrir", methods=["POST"])
@login_requerido
def abrir(capsula_id):
    capsula.abrir(capsula_id, session["usuario_id"])
    flash("💌 ¡Cápsula abierta! Tu yo del pasado te dejó este mensaje.", "ok")
    return redirect(url_for("capsulas.ver", capsula_id=capsula_id))


@bp.route("/capsulas/<int:capsula_id>/borrar", methods=["POST"])
@login_requerido
def borrar(capsula_id):
    capsula.borrar(capsula_id, session["usuario_id"])
    flash("Cápsula eliminada.", "ok")
    return redirect(url_for("capsulas.lista"))