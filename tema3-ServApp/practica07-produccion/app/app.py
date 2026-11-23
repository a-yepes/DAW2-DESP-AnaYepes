import os

from flask import Flask
from flask_wtf.csrf import CSRFProtect

from controllers import auth, capsulas, main

# Creamos la aplicación
app = Flask(__name__)

# Clave para firmar las cookies de sesión (viene del .env a través del docker-compose)
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]

# Protección CSRF: todos los formularios POST deben llevar un token secreto
CSRFProtect(app)

# Registramos los controladores (cada uno aporta sus rutas)
app.register_blueprint(main.bp)
app.register_blueprint(auth.bp)
app.register_blueprint(capsulas.bp)