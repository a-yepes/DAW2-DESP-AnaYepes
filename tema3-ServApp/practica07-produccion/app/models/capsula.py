from db import consultar, consultar_uno


def muro():
    """Cápsulas abiertas, públicas y no ocultas, con el nombre de su autor."""
    return consultar(
        """SELECT c.titulo, c.mensaje, c.emocion, c.abierta_en, u.nombre AS autor
           FROM capsulas c
           JOIN usuarios u ON u.id = c.usuario_id
           WHERE c.publica = 1 AND c.abierta = 1 AND c.oculta = 0
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