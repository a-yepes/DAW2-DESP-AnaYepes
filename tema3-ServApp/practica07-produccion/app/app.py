from flask import Flask

# Creamos la aplicación Flask
app = Flask(__name__)


# Ruta de la portada: cuando alguien visita "/", Flask ejecuta esta función
@app.route("/")
def inicio():
    return "<h1>⏳ TimeFlies</h1><p>Flask funcionando detrás de Nginx.</p>"