import os

from flask import Flask

from controllers import main

# Creamos la aplicación
app = Flask(__name__)

# Clave para firmar las cookies de sesión (viene del .env a través del docker-compose)
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]

# Registramos los controladores (cada uno aporta sus rutas)
app.register_blueprint(main.bp)