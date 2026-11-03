## Cuestiones finales

### 1. ¿Cuál es la función de Flask?

Flask es un framework de Python que permite desarrollar aplicaciones web, gestionar rutas HTTP y generar respuestas para los clientes.

### 2. ¿Cuál es la función de Gunicorn?

Gunicorn es un servidor WSGI que ejecuta aplicaciones Python y procesa las peticiones recibidas.

### 3. ¿Por qué no se utiliza Flask directamente en producción?

Porque el servidor de desarrollo de Flask está pensado para pruebas y desarrollo. En producción se recomienda utilizar un servidor WSGI como Gunicorn, preparado para gestionar las peticiones de forma más adecuada.

### 4. ¿Qué ventajas proporciona Gunicorn?

Permite utilizar varios workers, gestionar peticiones concurrentes, ejecutar aplicaciones WSGI y generar registros de acceso y errores.

### 5. ¿Qué función realiza Nginx?

Nginx recibe las peticiones HTTP de los clientes y las reenvía al servidor de aplicaciones. También puede gestionar conexiones y servir contenido estático.

### 6. ¿Qué es un Reverse Proxy?

Es un servidor intermediario que recibe las peticiones de los clientes y las reenvía a otro servidor interno, devolviendo posteriormente las respuestas al cliente.

### 7. ¿Qué ventajas aporta systemd?

Permite administrar los servicios, iniciarlos automáticamente, detenerlos, reiniciarlos, recuperarlos ante fallos y consultar sus registros.

### 8. ¿Qué diferencias existen entre Tomcat y Gunicorn?

Tomcat es un contenedor de servlets diseñado para aplicaciones Java, mientras que Gunicorn es un servidor WSGI diseñado para ejecutar aplicaciones Python.

### 9. ¿Qué similitudes existen entre Nginx + Tomcat y Nginx + Gunicorn?

Ambas arquitecturas utilizan Nginx como servidor web frontal y Reverse Proxy. Nginx recibe las peticiones y las reenvía al servidor de aplicaciones correspondiente.

### 10. ¿Qué mejoras podrían realizarse sobre la arquitectura implementada?

Se podrían incorporar HTTPS mediante certificados SSL/TLS, balanceo de carga, varios servidores Gunicorn, monitorización, medidas de seguridad adicionales y una política de copias de seguridad.

