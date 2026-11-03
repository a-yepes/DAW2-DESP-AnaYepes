# Práctica 3. 

## Objetivo.

En esta práctica desplegamos una aplicación web desarrollada con Python y Flask, utilizando Gunicorn como servidor WSGI y Nginx como servidor web y proxy inverso.

Para ello, utilizamos contenedores Docker gestionados mediante Docker Compose. Además, configuramos Gunicorn como servicio del sistema utilizando systemd en Ubuntu mediante WSL2.

El objetivo es conseguir que la aplicación esté disponible a través de Nginx.

Todas las evidencias pueden consultarse en la carpeta capturas.

## Tarea 1. Preparación de la estructura de trabajo

La estructura creada es la siguiente:

```text
tema3-ServApp/
└── practica03-flask-gunicorn/
    ├── aplicacion/
    │   ├── __init__.py
    │   └── app.py
    │
    ├── configuracion/
    │   ├── gunicorn.conf.py
    │   ├── nginx.conf
    │   ├── Dockerfile
    │   ├── compose.yaml
    │   └── gunicorn.service
    │
    ├── capturas/
    ├── requisitos.md
    ├── README.md
    ├── memoria.md
    
```

- **aplicacion/**: contiene el código Python de la aplicación Flask.
- **configuracion/**: contiene los archivos necesarios para configurar Gunicorn, Nginx, Docker y systemd.
- **capturas/**: almacena las capturas de pantalla realizadas durante las pruebas.
- **requisitos.md**: contiene las dependencias necesarias para ejecutar la aplicación.
- **README.md**: documenta el desarrollo y funcionamiento del proyecto.
- **memoria.md**: recoge las explicaciones y evidencias de la práctica.

---

## Tarea 2. Creación de una aplicación Flask

Es una aplicación web sencilla utilizando Python y el framework Flask.

La aplicación se encuentra dentro del directorio `aplicacion/` y permite mostrar una página de bienvenida e información relacionada con la práctica.

Se han creado tres rutas principales:

| Ruta | Función |
|---|---|
| `/` | Muestra la página principal de bienvenida e identifica a la alumna. |
| `/health` | Comprueba que la aplicación funciona correctamente. |
| `/info` | Muestra información sobre la alumna, el módulo y las tecnologías utilizadas. |

La ruta `/health` devuelve una respuesta en formato JSON:

```json
{
  "estado": "OK",
  "aplicacion": "Flask",
  "practica": "Practica 3"
}
```

La ruta `/info` proporciona información adicional sobre la aplicación, como las tecnologías utilizadas y la fecha de consulta.

Para desarrollar la aplicación se ha utilizado Flask, que permite definir rutas y gestionar las peticiones HTTP de una forma sencilla.

**Comprobación:** se ha verificado que la aplicación responde correctamente a las peticiones y que sus diferentes rutas están disponibles.


---

## Tarea 3. Configuración de Gunicorn

Gunicorn es un servidor WSGI que permite ejecutar aplicaciones web desarrolladas con Python, como la aplicación Flask creada en esta práctica.

Utilizamos Gunicorn para ejecutar la aplicación sin depender del servidor de desarrollo integrado de Flask.

El archivo `configuracion/gunicorn.conf.py` establece los parámetros de funcionamiento:

```python
bind = "0.0.0.0:8000"
workers = 2
timeout = 30
accesslog = "-"
errorlog = "-"
capture_output = True
loglevel = "info"
```

- **bind:** dirección y puerto donde escucha Gunicorn.
- **workers:** número de procesos trabajadores, en este caso dos.
- **timeout:** tiempo máximo de espera de una petición.
- **accesslog:** permite mostrar los registros de acceso.
- **errorlog:** permite mostrar los registros de errores.
- **capture_output:** recoge la salida de la aplicación.
- **loglevel:** establece el nivel de detalle de los registros.

Gunicorn se ejecuta utilizando el siguiente comando dentro del contenedor:

```bash
gunicorn --config gunicorn.conf.py aplicacion.app:app
```

La aplicación queda disponible en el puerto 8000.

**Comprobación:** se ha verificado que Gunicorn inicia correctamente, crea sus procesos trabajadores y permanece escuchando peticiones.

También se ha comprobado el acceso directo mediante:

```bash
curl.exe http://localhost:8000/health
```

Así confirmamos que Flask está funcionando a través de Gunicorn.

---

## Tarea 4. Configuración de Nginx

Nginx es un servidor web que se ha configurado para actuar como Reverse Proxy o proxy inverso.

Su función es recibir las peticiones HTTP de los clientes y reenviarlas al servidor Gunicorn, donde se ejecuta la aplicación Flask.

La configuración está en el archivo:

```text
configuracion/nginx.conf
```

```nginx
server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://app:8000;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Explicación:

- **listen 80:** indica que Nginx escucha en el puerto 80 dentro del contenedor.
- **server_name:** identifica el nombre del servidor.
- **location /**: establece que las peticiones recibidas se gestionan desde esta ubicación.
- **proxy_pass:** reenvía las peticiones al servicio Gunicorn.
- **proxy_set_header:** transmite información sobre la petición original, como el host, la dirección IP del cliente y el protocolo utilizado.

La dirección `http://app:8000` permite que Nginx se comunique con el servicio de Gunicorn mediante el nombre del servicio definido en Docker Compose.

**Comprobación:** se ha comprobado que Nginx inicia correctamente y que utiliza la configuración establecida para reenviar las peticiones a Gunicorn.

---

## Tarea 5. Verificación del flujo completo

Una vez configurados Flask, Gunicorn y Nginx, comprobamos que la comunicación entre los diferentes componentes funciona correctamente.

El flujo de las peticiones es el siguiente:

```text
        Usuario
           |
           v
         Nginx
       Puerto 8080
           |
           v
       Gunicorn
       Puerto 8000
           |
           v
         Flask
```

1. El usuario accede a la aplicación desde el navegador.
2. Nginx recibe la petición HTTP a través del puerto 8080.
3. Nginx reenvía la petición a Gunicorn.
4. Gunicorn ejecuta la aplicación Flask.
5. Flask genera la respuesta y esta vuelve al usuario a través de Gunicorn y Nginx.

Para gestionar los servicios utilizamos Docker Compose mediante el archivo `configuracion/compose.yaml`.

Con dos servicios:

| Servicio | Contenedor | Puerto publicado |
|---|---|---|
| Flask con Gunicorn | `flask_gunicorn` | 8000 |
| Nginx | `nginx_flask` | 8080 |

Para construir y arrancar los contenedores se ejecuta:

```bash
docker compose -f configuracion/compose.yaml up -d --build
```

Para comprobar que están funcionando:

```bash
docker ps
```

Pruebas:

**Acceso directo mediante Gunicorn:**

```bash
curl.exe http://localhost:8000/health
```

**Acceso a través de Nginx:**

```bash
curl.exe http://localhost:8080/health
```

En ambos casos se obtiene una respuesta JSON con el estado `OK` y un código HTTP 200.

Esto demuestra que la aplicación funciona y que Nginx puede comunicarse correctamente con Gunicorn.

---

## Tarea 6. Análisis de componentes

### Flask

Flask es un framework web desarrollado para Python que permite crear aplicaciones web mediante rutas y funciones.

En esta práctica se utiliza para desarrollar la aplicación, mostrar la página de bienvenida y proporcionar información mediante las rutas `/`, `/health` e `/info`.

Su función principal es gestionar la lógica de la aplicación y generar las respuestas que recibe el usuario.

### Gunicorn

Gunicorn es un servidor WSGI que permite ejecutar aplicaciones web desarrolladas con Python.

En esta práctica se encarga de ejecutar Flask y atender las peticiones que recibe desde Nginx.

Se ha configurado con dos procesos trabajadores (*workers*), permitiendo gestionar varias peticiones mediante diferentes procesos.

**Diferencia entre Flask y Gunicorn:**

Flask es el framework con el que se desarrolla la aplicación, mientras que Gunicorn es el servidor encargado de ejecutarla y atender las peticiones HTTP mediante WSGI.

### Nginx

Nginx es un servidor web que se utiliza en esta práctica como proxy inverso.

Recibe las peticiones de los usuarios y las reenvía a Gunicorn, que ejecuta la aplicación Flask.

Entre sus ventajas destacan:

- Permite actuar como intermediario entre los usuarios y la aplicación.
- Oculta el acceso directo al servidor de aplicaciones.
- Puede gestionar conexiones HTTP.
- Permite centralizar la entrada de peticiones.
- Facilita la incorporación de otras funciones, como HTTPS, balanceo de carga y caché.

**Conclusión del análisis:**

Si tuviéramos un restaurante, Nginx sería el recepcionista, porque es lo primero con lo que se topa el cliente (recibe peticiones HTTP), Gunicorn el jefe de sala, haciendo de intermediario entre el nginx y flask, y Flask el chef que cocina la respuesta (lee codigo).

Las tres tecnologías tienen funciones diferentes y complementarias: Flask desarrolla la aplicación, Gunicorn la ejecuta y Nginx recibe y distribuye las peticiones hacia el servidor de aplicaciones.

---

## Tarea 7. Creación de un servicio systemd

**systemd** es el sistema de inicialización y gestión de servicios utilizado en muchas distribuciones Linux. Permite iniciar, detener, reiniciar y supervisar servicios.

Para realizar esta tarea se ha utilizado Ubuntu mediante WSL2. He tenido que instalarlo con sudo apt install python3 python3-pip python3-venv -y.

El archivo

```text
/etc/systemd/system/flask-gunicorn.service
```

Explicación de las directivas:

- **User y Group:** indican el usuario y grupo con los que se ejecuta el servicio.
- **WorkingDirectory:** establece el directorio de trabajo donde se encuentra la aplicación.
- **Environment:** indica la ruta del entorno virtual de Python.
- **ExecStart:** establece el comando que inicia Gunicorn.
- **Restart=always:** indica que systemd debe intentar reiniciar el servicio cuando termine.
- **RestartSec=5:** establece una espera de cinco segundos antes de intentar reiniciarlo.

En esta configuración se utiliza el puerto 8001 para el servicio de systemd, evitando coincidir con el puerto 8000 utilizado por Gunicorn en Docker.

### Recargar la configuración

Después de crear o modificar el archivo se ejecuta:

```bash
sudo systemctl daemon-reload
```

### Habilitar el servicio

Para configurar su inicio automático:

```bash
sudo systemctl enable flask-gunicorn
```

### Iniciar el servicio

```bash
sudo systemctl start flask-gunicorn
```

### Comprobar el estado

```bash
sudo systemctl status flask-gunicorn
```

Obtenemos:

```text
Active: active (running)
```

### Detener el servicio

```bash
sudo systemctl stop flask-gunicorn
```

### Reiniciar el servicio

```bash
sudo systemctl restart flask-gunicorn
```

Así comprobamos que systemd permite gestionar el ciclo de vida del servicio Gunicorn.

---

## Tarea 8. Verificación de persistencia

En esta tarea se comprueba que el servicio Gunicorn está configurado para iniciarse automáticamente y que systemd puede gestionar su ejecución.

Para comprobar si el servicio está habilitado utilizamos:

```bash
sudo systemctl is-enabled flask-gunicorn
```

El resultado es:

```text
enabled
```

Esto significa que el servicio está habilitado para iniciarse automáticamente cuando arranque el sistema Linux.

También comprobamos su estado con:

```bash
sudo systemctl status flask-gunicorn
```

Para verificar el funcionamiento después de un reinicio del servicio utilizamos:

```bash
sudo systemctl restart flask-gunicorn
```

Y :

```bash
sudo systemctl status flask-gunicorn
```

---

## Tarea 9. Análisis de registros

### Logs de Gunicorn

Para consultar los registros de Gunicorn dentro de Docker se utiliza:

```bash
docker compose -f configuracion/compose.yaml logs app
```

En los registros se pueden identificar los siguientes elementos:

**Inicio de la aplicación**

Aparecen mensajes similares a:

```text
[INFO] Starting gunicorn 23.0.0
[INFO] Listening at: http://0.0.0.0:8000
[INFO] Booting worker with pid: 7
[INFO] Booting worker with pid: 8
```

Estos mensajes indican que Gunicorn se ha iniciado correctamente, está escuchando en el puerto 8000 y ha creado dos procesos trabajadores.

**Peticiones procesadas**

Se observan peticiones como:

```text
GET /health HTTP/1.1" 200
GET / HTTP/1.1" 200
```

El código HTTP 200 indica que las peticiones se han atendido correctamente.

**Posibles errores**

Durante las pruebas también pueden aparecer mensajes como:

```text
[CRITICAL] WORKER TIMEOUT
[ERROR] Error handling request
```

Estos mensajes indican que un trabajador ha superado el tiempo de espera o que se ha producido un problema durante el procesamiento de una petición.

También puede aparecer un error 404 cuando el navegador solicita `/favicon.ico` y la aplicación no dispone de ese recurso.

 ![Logs gunicorn](capturas/logs_gunicorn.png)

### Logs de Nginx

Para consultar los registros de Nginx se utiliza:

```bash
docker compose -f configuracion/compose.yaml logs nginx
```

**Accesos realizados**

Aparecen solicitudes como:

```text
"GET /health HTTP/1.1" 200
"GET / HTTP/1.1" 200
```

Esto demuestra que los usuarios han accedido a la aplicación a través de Nginx.

**Direcciones cliente**

En los registros aparece la dirección IP:

```text
172.20.0.1
```

Esta dirección corresponde a una dirección de la red interna de Docker desde la que Nginx recibe las solicitudes.

**Peticiones atendidas**

Durante las pruebas se han observado peticiones como:

| Petición | Código HTTP | Resultado |
|---|---|---|
| `GET /health` | 200 | Correcta. |
| `GET /` | 200 | Correcta. |
| `GET /favicon.ico` | 404 | Recurso no encontrado. |

El código 200 indica que la petición se ha procesado correctamente, mientras que el código 404 indica que el recurso solicitado no existe.

El análisis de los registros permite comprobar que Nginx recibe las peticiones y que Gunicorn ejecuta la aplicación Flask para generar las respuestas.

![Logs nginx](capturas/logs_nginx.png)

---

## Tarea 10. Comparación con Tomcat

### Arquitectura de la práctica anterior

```text
       Cliente
          |
          v
        Nginx
          |
          v
        Tomcat
          |
          v
    Aplicación Java
```

### Arquitectura de la práctica actual

```text
       Cliente
          |
          v
        Nginx
          |
          v
       Gunicorn
          |
          v
         Flask
```

La arquitectura anterior estaba formada por Nginx, Tomcat y una aplicación Java.

La arquitectura actual utiliza Nginx, Gunicorn y una aplicación Flask.

### Similitudes

- Ambas utilizan Nginx como servidor web frontal.
- Ambas utilizan un Reverse Proxy.
- Los servidores de aplicaciones ejecutan las aplicaciones correspondientes.
- Se separan las funciones del servidor web y del servidor de aplicaciones.

### Diferencias

- Tomcat está diseñado para aplicaciones Java.
- Gunicorn está diseñado para aplicaciones Python compatibles con WSGI.
- Tomcat funciona como contenedor de servlets.
- Gunicorn ejecuta aplicaciones Python mediante workers.

### Ventajas

Tomcat es especialmente adecuado para aplicaciones Java empresariales y tecnologías relacionadas con Jakarta Servlet.

Gunicorn destaca por su sencillez y su integración con frameworks Python como Flask.

Nginx puede utilizarse con ambas tecnologías, independientemente del lenguaje de programación de la aplicación.

---
## Problemas encontrados y soluciones
Me salia el error ModuleNotFoundError: No module named 'aplicacion'


El problema era que WorkingDirectory del archivo `flask-gunicorn.service` apuntaba al directorio incorrecto. 

Lo he solucionado corrigiendo la ruta de WorkingDirectory para que apuntase directamente a la carpeta practica03-flask-gunicorn.

Después he recargado y reiniciado con:

```bash
sudo systemctl daemon-reload
sudo systemctl restart flask-gunicorn
sudo systemctl status flask-gunicorn
```



