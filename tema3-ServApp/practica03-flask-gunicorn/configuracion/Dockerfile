FROM python:3.12-slim

WORKDIR /app

COPY ../requisitos.md /tmp/requisitos.md

RUN pip install --no-cache-dir -r /tmp/requisitos.md

COPY aplicacion/ ./aplicacion/

COPY configuracion/gunicorn.conf.py ./gunicorn.conf.py

EXPOSE 8000

CMD ["gunicorn", "--config", "gunicorn.conf.py", "aplicacion.app:app"]