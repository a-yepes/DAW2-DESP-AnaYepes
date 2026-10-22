# Despliegue automatizado de Flask en AWS EC2

Práctica de despliegue automatizado de una aplicación web Python/Flask en una instancia Ubuntu de AWS EC2.

## Objetivo

Crear un script User Data que configure automáticamente una instancia EC2 para servir una aplicación Flask mediante Apache y WSGI.

El archivo user_data.sh se introduce en el campo User Data durante el lanzamiento de la instancia EC2.

El script instala las dependencias, crea la aplicación Flask, configura Apache y activa el sitio.

Una vez finalizado el despliegue, la aplicación estará disponible mediante:

http://IP_PUBLICA

# ¿Qué hace user_data.sh?

El script automáticamente:

1. Actualiza los repositorios del sistema.
2. Instala Apache2.
3. Instala el módulo WSGI para Python 3.
4. Instala Flask.
5. Crea el directorio `/var/www/flaskapp/`.
6. Genera la aplicación Flask.
7. Genera el adaptador WSGI.
8. Genera la configuración del VirtualHost de Apache.
9. Activa el módulo WSGI.
10. Activa el sitio Flask.
11. Desactiva el sitio Apache por defecto.
12. Configura los permisos.
13. Comprueba la configuración de Apache.
14. Reinicia Apache.
