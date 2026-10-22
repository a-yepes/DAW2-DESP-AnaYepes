#!/bin/bash

# Script comprobado con bash -n 

# Actualizar repositorios
apt-get update -y

# Instalar Apache, WSGI para Python 3 y Flask
apt-get install -y apache2 libapache2-mod-wsgi-py3 python3-flask

# Crear directorio de la aplicación
mkdir -p /var/www/flaskapp

# Crear app.py
cat << 'EOF' > /var/www/flaskapp/app.py
from flask import Flask

application = Flask(__name__)

@application.route("/")
def inicio():
    return "Aplicación Flask en AWS de Ana Yepes y fecha 03/10/2026 desplegada automáticamente en AWS"

if __name__ == "__main__":
    application.run()
EOF

# Crear app.wsgi
cat << 'EOF' > /var/www/flaskapp/app.wsgi
import sys

sys.path.insert(0, "/var/www/flaskapp")

from app import application
EOF

# Crear configuración del VirtualHost
cat << 'EOF' > /etc/apache2/sites-available/flaskapp.conf
<VirtualHost *:80>

    WSGIScriptAlias / /var/www/flaskapp/app.wsgi

    <Directory /var/www/flaskapp>
        Require all granted
    </Directory>

</VirtualHost>
EOF

# Activar el módulo WSGI
a2enmod wsgi

# Activar el sitio Flask
a2ensite flaskapp.conf

# Desactivar el sitio por defecto de Apache
a2dissite 000-default.conf

# Asignar permisos adecuados
chown -R www-data:www-data /var/www/flaskapp
chmod 755 /var/www/flaskapp
chmod 644 /var/www/flaskapp/app.py
chmod 644 /var/www/flaskapp/app.wsgi

# Comprobar la configuración de Apache
apache2ctl configtest

# Reiniciar Apache
systemctl restart apache2