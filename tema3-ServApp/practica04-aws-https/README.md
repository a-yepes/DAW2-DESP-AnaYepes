# Práctica 4 

## 1. Introducción

En esta práctica desplegamos una aplicación web desarrollada con Flask en una instancia de Amazon EC2.

La aplicación se ha ejecutado mediante Docker y Gunicorn, utilizando Nginx como servidor web y proxy inverso para gestionar las peticiones HTTP y HTTPS.

Además, se ha configurado un certificado SSL autofirmado para permitir el acceso seguro a la aplicación mediante HTTPS.

## 2. Objetivos

Los objetivos principales de esta práctica son:

- Crear y configurar una instancia EC2 en AWS.
- Automatizar la instalación de herramientas mediante User Data.
- Instalar y utilizar Docker.
- Desplegar una aplicación Flask dentro de un contenedor.
- Utilizar Gunicorn como servidor WSGI.
- Instalar y configurar Nginx como proxy inverso.
- Generar un certificado SSL autofirmado.
- Configurar HTTPS para permitir conexiones seguras.
- Comprobar el funcionamiento de todos los componentes.

## 3. Arquitectura utilizada

La arquitectura utilizada está formada por un navegador web que se comunica con una instancia EC2 mediante HTTPS.

Dentro de la instancia EC2 se encuentra Nginx, que recibe las peticiones y las redirige hacia Gunicorn, encargado de ejecutar la aplicación Flask.

```text
                 INTERNET
                    |
                    |
                 HTTPS
                (443)
                    |
                    v
              +-----------+
              |   NGINX   |
              |  Reverse  |
              |   Proxy   |
              +-----------+
                    |
                    |
                    v
              +-----------+
              | GUNICORN  |
              |   WSGI    |
              +-----------+
                    |
                    |
                    v
              +-----------+
              |   FLASK   |
              |  app.py   |
              +-----------+
                    |
                    v
              Aplicación web
```

## 4. AWS EC2

Para realizar el despliegue he utilizado una instancia EC2 con Ubuntu.

Durante la creación de la instancia se han configurado:

En el grupo de seguridad he permitido los siguientes puertos:

| Puerto | Protocolo | Función |
|---|---|---|
| 22 | TCP | Acceso SSH |
| 80 | TCP | Acceso HTTP |
| 443 | TCP | Acceso HTTPS |


## 5. User Data

El script utilizado contiene los siguientes comandos:

```bash
#!/bin/bash

apt-get update -y

apt-get install -y docker.io git curl

systemctl enable docker
systemctl start docker

usermod -aG docker ubuntu

mkdir -p /opt/practica04
chmod 755 /opt/practica04
```

Este script permite:

- Actualizar los paquetes del sistema.
- Instalar Docker, Git y Curl.
- Activar Docker para que se inicie automáticamente.
- Iniciar el servicio Docker.
- Añadir el usuario ubuntu al grupo docker.
- Crear el directorio de trabajo `/opt/practica04`.

La finalidad de User Data es automatizar las tareas iniciales para facilitar la preparación de la instancia EC2.

## 6. Flask

Con Flask creo la aplicación web.

El archivo principal de la aplicación es `app.py`, donde se define la ruta principal que devuelve el contenido HTML.

El archivo `requirements.txt`, que contiene las dependencias necesarias para su ejecución.

Luego he copiado la aplicación a la instancia EC2 dentro del directorio:

```text
/opt/practica04
```

## 7. Gunicorn

Utilizo Gunicorn como servidor WSGI para ejecutar la aplicación Flask.

Gunicorn permite atender las peticiones de la aplicación sin utilizar el servidor de desarrollo integrado de Flask.

Se ha configurado para escuchar en el puerto 5000:

```bash
gunicorn --bind 0.0.0.0:5000 app:app
```

Gunicorn se ejecuta dentro del contenedor Docker junto con la aplicación Flask.

De esta forma, Nginx puede comunicarse con Gunicorn para enviarle las peticiones recibidas desde el navegador.

## 8. Nginx

He instalado Nginx directamente en la instancia EC2 mediante:

```bash
sudo apt update
sudo apt install nginx -y
```

Nginx se utiliza como proxy inverso para recibir las peticiones de los usuarios y redirigirlas hacia la aplicación Flask.

Se ha configurado para enviar las peticiones al puerto 5000:

```nginx
location / {
    proxy_pass http://127.0.0.1:5000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

Una vez realizada la configuración, compruebo que no existan errores con:

```bash
sudo nginx -t
```

Y reinicio el servicio:

```bash
sudo systemctl restart nginx
```

## 9. HTTPS

Para habilitar HTTPS he generado un certificado SSL autofirmado mediante OpenSSL.

Los archivos generados son:

```text
certificado.crt
clave.key
```

Posteriormente he modificado la configuración de Nginx para habilitar HTTPS en el puerto 443.

También he configurado una redirección para que las peticiones recibidas por el puerto 80 se envíen automáticamente al puerto 443.

La conexión se comprueba accediendo desde el navegador a:

```text
https://IP_PUBLICA
```

Al utilizar un certificado autofirmado, el navegador muestra una advertencia de seguridad. 

## 10. Evidencias obtenidas

Las evidencias se encuentran organizadas en el directorio:

```text
capturas/
```

## 11. Problemas encontrados 

Para comprobar que la aplicación Flask funcionaba directamente desde el navegador he tenido que abrir el puerto 5000 en el grupo de seguridad de EC2.

Sin esta regla, las conexiones externas al puerto 5000 eran bloqueadas por AWS, aunque el contenedor estuviese funcionando correctamente.

## 12. Soluciones aplicadas

Apertura del puerto 5000.

```text
Tipo: TCP personalizado
Puerto: 5000
Origen: Mi IP
```

Esto permitió acceder a la aplicación mediante:

```text
http://IP_PUBLICA:5000
```

Una vez comprobado que Flask funcionaba, el acceso definitivo se realizó mediante Nginx.

El puerto 5000 no debe permanecer abierto públicamente en la configuración final, ya que Nginx recibe las conexiones externas por los puertos 80 y 443 y las reenvía internamente al servicio Flask.

## 13. Conclusiones

En conclusión, esta práctica ha servido para conocer un proceso completo de despliegue de una aplicación Flask en la nube, desde la creación de la infraestructura hasta la configuración del acceso seguro mediante HTTPS.