import os
from datetime import date

from flask import Flask, jsonify

app = Flask(__name__)

# Sustituye estos valores por los datos reales de tu matrícula.
ALUMNA = "Ana Yepes"
CENTRO = "IES Pio Baroja"
CICLO = "Desarrollo de Aplicaciones Web (DAW)"
GRUPO = "2DAWBIL"

FECHA_DESPLIEGUE = os.getenv("DEPLOYMENT_DATE", date.today().isoformat())


@app.route("/")
def index():
    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Práctica UT2 - Proxy inverso SSL</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 60px auto;
                padding: 24px;
                background: #f3f6fa;
                color: #1f2937;
            }}
            main {{
                background: white;
                padding: 32px;
                border-radius: 12px;
                box-shadow: 0 4px 18px rgba(0,0,0,.08);
            }}
            h1 {{ color: #1756a9; }}
            li {{ margin: 12px 0; }}
            .estado {{ color: #147d43; font-weight: bold; }}
        </style>
    </head>
    <body>
        <main>
            <h1>Práctica UT2: Proxy inverso Nginx con SSL</h1>
            <p class="estado">Aplicación Flask operativa</p>
            <ul>
                <li><strong>Alumna:</strong> {ALUMNA}</li>
                <li><strong>Centro formativo:</strong> {CENTRO}</li>
                <li><strong>Ciclo:</strong> {CICLO}</li>
                <li><strong>Grupo:</strong> {GRUPO}</li>
                <li><strong>Fecha de despliegue:</strong> {23/10/2026}</li>
            </ul>
        </main>
    </body>
    </html>
    """


@app.route("/health")
def health():
    return jsonify(status="ok"), 200
