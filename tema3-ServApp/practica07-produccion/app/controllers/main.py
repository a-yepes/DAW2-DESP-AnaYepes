from flask import Blueprint, jsonify, render_template

from db import consultar_uno
from models import capsula

# Un Blueprint agrupa rutas relacionadas. Este es el controlador "principal".
bp = Blueprint("main", __name__)


@bp.route("/")
def inicio():
    # 1) pide los datos al MODELO   2) se los pasa a la VISTA
    return render_template(
        "index.html",
        muro=capsula.muro(),
        contadores=capsula.contadores(),
        emociones=capsula.EMOCIONES,
    )


@bp.route("/salud")
def salud():
    """Comprobación técnica: si responde, Flask funciona y conecta con MariaDB."""
    fila = consultar_uno("SELECT VERSION() AS version")
    return jsonify(estado="ok", app="TimeFlies", mariadb=fila["version"])