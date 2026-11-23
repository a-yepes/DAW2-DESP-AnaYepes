import os

import pymysql


def conectar():
    """Abre una conexión con MariaDB usando las variables de entorno del docker-compose."""
    return pymysql.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"],
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,  # cada fila llega como diccionario: fila["titulo"]
        autocommit=True,                         # cada INSERT/UPDATE se guarda al momento
    )


def consultar(sql, parametros=()):
    """SELECT que devuelve VARIAS filas (lista de diccionarios)."""
    conexion = conectar()
    try:
        with conexion.cursor() as cursor:
            cursor.execute(sql, parametros)
            return cursor.fetchall()
    finally:
        conexion.close()


def consultar_uno(sql, parametros=()):
    """SELECT que devuelve UNA fila (un diccionario, o None si no hay)."""
    conexion = conectar()
    try:
        with conexion.cursor() as cursor:
            cursor.execute(sql, parametros)
            return cursor.fetchone()
    finally:
        conexion.close()


def ejecutar(sql, parametros=()):
    """INSERT, UPDATE o DELETE. Devuelve el id de la fila insertada."""
    conexion = conectar()
    try:
        with conexion.cursor() as cursor:
            cursor.execute(sql, parametros)
            return cursor.lastrowid
    finally:
        conexion.close()