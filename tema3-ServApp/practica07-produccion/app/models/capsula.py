from db import consultar, consultar_uno, ejecutar

# Emociones disponibles: clave que se guarda en la BBDD -> (icono, nombre visible)
EMOCIONES = {
    "ilusion": ("✨", "Ilusión"),
    "nostalgia": ("🍂", "Nostalgia"),
    "gratitud": ("💛", "Gratitud"),
    "reto": ("🎯", "Reto"),
    "humor": ("😂", "Humor"),
    "calma": ("🌊", "Calma"),
}


def muro():
    """Cápsulas abiertas y públicas con el nombre de su autor."""
    return consultar(
        """SELECT c.titulo, c.mensaje, c.emocion, c.abierta_en, u.nombre AS autor
           FROM capsulas c
           JOIN usuarios u ON u.id = c.usuario_id
           WHERE c.publica = 1 AND c.abierta = 1
           ORDER BY c.abierta_en DESC"""
    )


def contadores():
    """Totales para la portada: cuántas cápsulas hay, selladas y abiertas."""
    return consultar_uno(
        """SELECT COUNT(*) AS total,
                  COALESCE(SUM(abierta = 0), 0) AS selladas,
                  COALESCE(SUM(abierta = 1), 0) AS abiertas
           FROM capsulas"""
    )


def es_fecha_futura(fecha):
    """Pregunta a MariaDB si la fecha es posterior a ahora (la hora oficial la da la BBDD)."""
    fila = consultar_uno("SELECT %s > NOW() AS futura", (fecha,))
    return fila["futura"] == 1


def crear(usuario_id, titulo, mensaje, emocion, fecha_apertura, publica):
    """Guarda una cápsula nueva (sellada). Devuelve su id."""
    return ejecutar(
        """INSERT INTO capsulas (usuario_id, titulo, mensaje, emocion, fecha_apertura, publica)
           VALUES (%s, %s, %s, %s, %s, %s)""",
        (usuario_id, titulo, mensaje, emocion, fecha_apertura, publica),
    )


def de_usuario(usuario_id):
    """Cápsulas de un usuario. 'lista' vale 1 si ya ha llegado su fecha de apertura."""
    return consultar(
        """SELECT id, titulo, emocion, fecha_apertura, abierta, abierta_en,
                  fecha_apertura <= NOW() AS lista
           FROM capsulas
           WHERE usuario_id = %s
           ORDER BY abierta, fecha_apertura""",
        (usuario_id,),
    )


def por_id(capsula_id, usuario_id):
    """Una cápsula concreta, SOLO si pertenece a ese usuario (si no, devuelve None)."""
    return consultar_uno(
        """SELECT *, fecha_apertura <= NOW() AS lista
           FROM capsulas
           WHERE id = %s AND usuario_id = %s""",
        (capsula_id, usuario_id),
    )


def abrir(capsula_id, usuario_id):
    """Marca la cápsula como abierta. El WHERE impide abrirla antes de su fecha."""
    ejecutar(
        """UPDATE capsulas SET abierta = 1, abierta_en = NOW()
           WHERE id = %s AND usuario_id = %s AND abierta = 0 AND fecha_apertura <= NOW()""",
        (capsula_id, usuario_id),
    )


def borrar(capsula_id, usuario_id):
    """Elimina la cápsula (solo si es de ese usuario)."""
    ejecutar("DELETE FROM capsulas WHERE id = %s AND usuario_id = %s", (capsula_id, usuario_id))