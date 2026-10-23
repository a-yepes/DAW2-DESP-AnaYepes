
from datetime import date
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def inicio():
    fecha = date.today().strftime("%d/%m/%Y")

    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Práctica UT2 - Proxy Inverso Nginx</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f2f4f8;
                margin: 0;
                padding: 40px 20px;
            }}
            main {{
                max-width: 700px;
                margin: auto;
                padding: 30px;
                background: white;
                border-radius: 12px;
                box-shadow: 0 4px 12px #0002;
            }}
            h1 {{ color: #174a7e; }}
            p {{ font-size: 18px; }}
        </style>
    </head>
    <body>
        <main>
            <h1>Práctica UT2: Proxy Inverso Nginx</h1>
            <p><strong>Nombre y apellidos:</strong> Ana Yepes Campillo</p>
            <p><strong>Centro educativo:</strong> IES Pio Baroja </p>
            <p><strong>Ciclo, curso y grupo:</strong> 2DAWBIL</p>
            <p><strong>Fecha de despliegue:</strong> {fecha}</p>
            <p>Aplicación Flask funcionando detrás de Nginx con HTTPS.</p>
        </main>
    </body>
    </html>
    """

@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200
