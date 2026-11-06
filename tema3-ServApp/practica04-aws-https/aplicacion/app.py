
from flask import Flask

app = Flask(__name__)

@app.route("/")
def inicio():
    return """
    <h1>Practica 04 - AWS EC2</h1>
    <p>Aplicacion Flask funcionando correctamente.</p>
    <p>Desplegada con Docker, Gunicorn y Nginx.</p>
    """

if __name__ == "__main__":
    app.run()
