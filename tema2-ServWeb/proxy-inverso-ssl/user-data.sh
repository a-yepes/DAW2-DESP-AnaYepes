#!/bin/bash
set -Eeuo pipefail

exec > >(tee -a /var/log/user-data-proxy-ssl.log) 2>&1

echo "=== Inicio del despliegue UT2 ==="

export DEBIAN_FRONTEND=noninteractive

apt-get update
apt-get install -y ca-certificates curl openssl

# Instalar Docker Engine y el plugin Docker Compose desde el repositorio oficial.
install -m 0755 -d /etc/apt/keyrings

curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
  -o /etc/apt/keyrings/docker.asc

chmod a+r /etc/apt/keyrings/docker.asc

. /etc/os-release

echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu ${UBUNTU_CODENAME:-$VERSION_CODENAME} stable" \
  > /etc/apt/sources.list.d/docker.list

apt-get update

apt-get install -y \
  docker-ce \
  docker-ce-cli \
  containerd.io \
  docker-buildx-plugin \
  docker-compose-plugin

systemctl enable --now docker

# Crear la estructura de despliegue.
mkdir -p /opt/proxy-inverso-ssl/app
mkdir -p /opt/proxy-inverso-ssl/nginx/certs

cd /opt/proxy-inverso-ssl

# Obtener la IP pública usando IMDSv2.
TOKEN=$(curl -fsS -X PUT \
  "http://169.254.169.254/latest/api/token" \
  -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")

PUBLIC_IP=$(curl -fsS \
  -H "X-aws-ec2-metadata-token: $TOKEN" \
  "http://169.254.169.254/latest/meta-data/public-ipv4")

# Generar un certificado autofirmado válido para la IP pública.
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout nginx/certs/privkey.pem \
  -out nginx/certs/fullchain.pem \
  -subj "/CN=${PUBLIC_IP}" \
  -addext "subjectAltName=IP:${PUBLIC_IP}"

chmod 600 nginx/certs/privkey.pem

# Guardar la fecha de despliegue.
echo "DEPLOYMENT_DATE=$(date -u +%F)" > .env
chmod 600 .env

# Aplicación Flask.
cat > app/app.py <<'PYEOF'
import os
from datetime import date
from flask import Flask, jsonify

app = Flask(__name__)

ALUMNA = "Ana Yepes"
CENTRO = "IES Pio Baroja"
CICLO = "Desarrollo de Aplicaciones Web (DAW)"
GRUPO = "2DAWBIL"
FECHA_DESPLIEGUE = os.getenv("DEPLOYMENT_DATE", date.today().isoformat())

@app.route("/")
def index():
    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>Práctica UT2 - Proxy inverso SSL</title>
    </head>
    <body style="font-family:Arial,sans-serif;max-width:800px;margin:60px auto;padding:24px">
      <h1>Práctica UT2: Proxy inverso Nginx con SSL</h1>
      <p>Aplicación Flask operativa</p>
      <ul>
        <li><strong>Alumna:</strong> {ALUMNA}</li>
        <li><strong>Centro:</strong> {CENTRO}</li>
        <li><strong>Ciclo:</strong> {CICLO}</li>
        <li><strong>Grupo:</strong> {GRUPO}</li>
        <li><strong>Fecha de despliegue:</strong> {FECHA_DESPLIEGUE}</li>
      </ul>
    </body>
    </html>
    """

@app.route("/health")
def health():
    return jsonify(status="ok"), 200
PYEOF

cat > app/requirements.txt <<'REQEOF'
Flask==3.1.2
gunicorn==23.0.0
REQEOF

# Configuración de Nginx.
cat > nginx/default.conf <<'NGINXEOF'
server {
    listen 80;
    server_name _;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name _;

    ssl_certificate /etc/nginx/certs/fullchain.pem;
    ssl_certificate_key /etc/nginx/certs/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers off;
    server_tokens off;

    location / {
        proxy_pass http://flask:5000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
NGINXEOF

# Docker Compose: Flask solo está accesible por la red privada.
cat > docker-compose.yml <<'COMPOSEEOF'
services:
  flask:
    image: python:3.12-slim
    container_name: ut2-flask
    working_dir: /app
    command: >
      sh -c "pip install --no-cache-dir -r requirements.txt &&
             gunicorn --bind 0.0.0.0:5000 --workers 2 app:app"
    env_file:
      - .env
    volumes:
      - ./app:/app:ro
    networks:
      - red_privada
    restart: unless-stopped

  nginx:
    image: nginx:1.28-alpine
    container_name: ut2-nginx
    depends_on:
      - flask
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/default.conf:/etc/nginx/conf.d/default.conf:ro
      - ./nginx/certs:/etc/nginx/certs:ro
    networks:
      - red_privada
    restart: unless-stopped

networks:
  red_privada:
    driver: bridge
COMPOSEEOF

# Validar la configuración y arrancar los servicios.
docker compose config
docker compose up -d

echo "=== Estado de los contenedores ==="
docker compose ps

echo "=== Despliegue finalizado ==="
echo "IP pública: ${PUBLIC_IP}"