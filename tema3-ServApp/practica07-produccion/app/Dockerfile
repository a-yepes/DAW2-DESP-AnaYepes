# Imagen base: Python 3.12 en versión ligera
FROM python:3.12-slim

# Carpeta de trabajo dentro del contenedor
WORKDIR /app

# 1º copiamos solo requirements.txt e instalamos las librerías.
# (Si el código cambia pero las librerías no, Docker reutiliza esta capa y construye más rápido)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2º copiamos el resto del código de la aplicación
COPY . .

# Flask escucha en el puerto 5000 (solo dentro de la red de Docker)
EXPOSE 5000

# Gunicorn: servidor de aplicaciones para producción. "app:app" = archivo app.py, variable app
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]