# UT2 --- Proxy inverso Nginx, Flask y HTTPS

## 1. Descripción

Práctica de despliegue de una aplicación Flask detrás de Nginx, con
Docker Compose y HTTPS mediante Let's Encrypt.

-   **Dominio:** `despliegueayc.duckdns.org`
-   **Proxy inverso:** Nginx
-   **Aplicación:** Flask en el puerto interno `5000`
-   **Contenedores:** `ut2-nginx` y `ut2-flask`
-   **Puertos publicados:** `80` (HTTP) y `443` (HTTPS)

## 2. Estructura del proyecto

Estructura esperada según la configuración trabajada:

``` text
/opt/proxy-inverso-ssl/
├── docker-compose.yml
├── nginx/
│   ├── default.conf
│   └── certs/                 # Certificado anterior, si se conserva
├── certbot/
│   └── www/
│       └── .well-known/acme-challenge/
├── letsencrypt/
│   ├── live/
│   ├── archive/
│   └── renewal/
└── README.md
```

No publiques `privkey.pem` ni otros secretos en un repositorio público.

## 3. Requisitos

-   Ubuntu, Docker y Docker Compose.
-   DNS de `despliegueayc.duckdns.org` apuntando a la IP pública de la
    instancia.
-   Tráfico entrante permitido en los puertos TCP `80` y `443`.
-   En esta instancia se utilizan comandos Docker con `sudo`.

## 4. Scripts y comandos de administración

Estos son los comandos utilizados para administrar el proyecto; no se
presupone que existan scripts `.sh` independientes.

### Entrar al directorio

``` bash
cd /opt/proxy-inverso-ssl
```

### Iniciar los servicios

``` bash
sudo docker compose up -d
```

### Ver el estado de los contenedores

``` bash
sudo docker compose ps
```

### Validar la configuración de Nginx

``` bash
sudo docker compose exec nginx nginx -t
```

### Recargar Nginx después de un cambio

``` bash
sudo docker compose exec nginx nginx -s reload
```

Antes de recargar, conviene ejecutar `nginx -t`.

### Consultar registros

``` bash
sudo docker compose logs --tail=100 nginx
sudo docker compose logs --tail=100 flask
```

Para seguirlos en tiempo real:

``` bash
sudo docker compose logs -f nginx flask
```

Si el servicio Flask tiene otro nombre en `docker-compose.yml`,
sustituye `flask` por el nombre real.

### Comprobar redirección HTTP a HTTPS

``` bash
curl -I http://despliegueayc.duckdns.org
```

### Comprobar HTTPS

``` bash
curl -Iv https://despliegueayc.duckdns.org
```

Inspeccionar el certificado que presenta el servidor:

``` bash
echo | openssl s_client \
  -connect despliegueayc.duckdns.org:443 \
  -servername despliegueayc.duckdns.org 2>/dev/null \
  | openssl x509 -noout -issuer -subject -dates
```

### Probar el webroot de Let's Encrypt

Crear un archivo de prueba:

``` bash
sudo mkdir -p /opt/proxy-inverso-ssl/certbot/www/.well-known/acme-challenge
echo "prueba-letsencrypt" | sudo tee /opt/proxy-inverso-ssl/certbot/www/.well-known/acme-challenge/test
```

Comprobarlo:

``` bash
curl http://despliegueayc.duckdns.org/.well-known/acme-challenge/test
```

La respuesta esperada es `prueba-letsencrypt`. No solicites de nuevo el
certificado hasta que esta ruta funcione correctamente.

### Comando de Certbot utilizado

``` bash
sudo docker run --rm \
  -v /opt/proxy-inverso-ssl/letsencrypt:/etc/letsencrypt \
  -v /opt/proxy-inverso-ssl/libletsencrypt:/var/lib/letsencrypt \
  -v /opt/proxy-inverso-ssl/certbot/www:/var/www/certbot \
  certbot/certbot certonly \
  --webroot -w /var/www/certbot \
  -d despliegueayc.duckdns.org \
  --email a.yepescampillo@gmail.com \
  --agree-tos --no-eff-email
```

**Nota:** el primer intento de Certbot falló con `unauthorized` y una
respuesta `404` para la validación ACME. Por ello, el comando no
demuestra por sí solo que el certificado se haya emitido. Verifica que
Certbot termina correctamente y que los archivos existen antes de
configurar Nginx para usarlos.

## 5. Configuración de Nginx

El archivo `nginx/default.conf` debe configurar:

-   Un servidor HTTP en el puerto `80`.
-   Una ubicación para `/.well-known/acme-challenge/` que sirva archivos
    desde `/var/www/certbot`.
-   Redirección del resto de peticiones HTTP a HTTPS.
-   Un servidor HTTPS en el puerto `443`.
-   El certificado y la clave privada.
-   El proxy inverso hacia `http://flask:5000`.

Ejemplo de directivas del proxy:

``` nginx
location / {
    proxy_pass http://flask:5000;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

Si se usa el certificado de Let's Encrypt, las rutas dentro del
contenedor son:

``` nginx
ssl_certificate /etc/letsencrypt/live/despliegueayc.duckdns.org/fullchain.pem;
ssl_certificate_key /etc/letsencrypt/live/despliegueayc.duckdns.org/privkey.pem;
ssl_protocols TLSv1.2 TLSv1.3;
```

En `docker-compose.yml`, el servicio Nginx debe montar el directorio de
certificados:

``` yaml
- ./letsencrypt:/etc/letsencrypt:ro
```

Hay que montar el directorio completo `letsencrypt/`, porque `live/`
contiene enlaces simbólicos que apuntan a `archive/`.

