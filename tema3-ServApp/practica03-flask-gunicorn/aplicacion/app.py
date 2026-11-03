from flask import jsonify
from datetime import datetime


def register_routes(app):

    @app.route("/")
    def inicio():
        return """
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <title>Práctica 3 - Flask</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background: #f0f2f5;
                    text-align: center;
                    padding: 60px;
                }

                .contenedor {
                    background: white;
                    padding: 35px;
                    border-radius: 15px;
                    max-width: 650px;
                    margin: auto;
                    box-shadow: 0 4px 12px #cccccc;
                }

                h1 {
                    color: #2471a3;
                }

                .correcto {
                    color: green;
                    font-weight: bold;
                }
            </style>
        </head>

        <body>
            <div class="contenedor">
                <h1>¡Bienvenido a mi aplicación Flask!</h1>

                <h2>Práctica 3 - Despliegue de aplicaciones</h2>

                <p><strong>Alumna:</strong> Ana Yepes</p>

                <p><strong>Módulo:</strong> Despliegue de Aplicaciones Web</p>

                <p><strong>Tecnologías:</strong></p>

                <p>Python + Flask + Gunicorn + Nginx</p>

                <p class="correcto">
                    Aplicación funcionando correctamente.
                </p>
            </div>
        </body>
        </html>
        """


    @app.route("/health")
    def health():
        return jsonify({
            "estado": "OK",
            "aplicacion": "Flask",
            "practica": "Practica 3"
        }), 200


    @app.route("/info")
    def info():
        return jsonify({
            "alumna": "Ana Yepes",
            "modulo": "Despliegue de Aplicaciones Web",
            "tecnologias": [
                "Python",
                "Flask",
                "Gunicorn",
                "Nginx"
            ],
            "fecha": datetime.now().isoformat()
        })


app = Flask(__name__)

register_routes(app)