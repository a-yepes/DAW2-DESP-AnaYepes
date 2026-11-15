
import os
import time
import pymysql

from flask import Flask, render_template_string

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "mariadb")
DB_NAME = os.getenv("DB_NAME", "practica05AnaYepes")
DB_USER = os.getenv("DB_USER", "appuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")


def conectar_bd():
    for intento in range(10):
        try:
            return pymysql.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME,
                cursorclass=pymysql.cursors.DictCursor,
                connect_timeout=5
            )
        except pymysql.MySQLError:
            if intento == 9:
                raise
            time.sleep(3)


@app.route("/")
def inicio():
    conexion = conectar_bd()

    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM tareas ORDER BY id")
            tareas = cursor.fetchall()
    finally:
        conexion.close()

    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Práctica 05 - Ana Yepes</title>
        <style>
            body {
                font-family: Arial;
                margin: 40px;
                background: #f2f2f2;
            }
            h1 { color: #263b59; }
            table {
                border-collapse: collapse;
                width: 100%;
                background: white;
            }
            th, td {
                border: 1px solid #ddd;
                padding: 12px;
                text-align: left;
            }
            th {
                background: #263b59;
                color: white;
            }
        </style>
    </head>
    <body>
        <h1>Práctica 05 - Docker Compose</h1>
        <h2>Listado de tareas almacenadas en MariaDB</h2>
        <table>
            <tr>
                <th>ID</th>
                <th>Título</th>
                <th>Descripción</th>
                <th>Estado</th>
            </tr>
            {% for tarea in tareas %}
            <tr>
                <td>{{ tarea.id }}</td>
                <td>{{ tarea.titulo }}</td>
                <td>{{ tarea.descripcion }}</td>
                <td>{{ tarea.estado }}</td>
            </tr>
            {% endfor %}
        </table>
        <p>Total de tareas: {{ tareas|length }}</p>
    </body>
    </html>
    """

    return render_template_string(html, tareas=tareas)


@app.route("/health")
def health():
    return "OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
