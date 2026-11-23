from werkzeug.security import check_password_hash, generate_password_hash

from db import consultar_uno, ejecutar


def buscar_por_email(email):
    """Devuelve el usuario con ese email (diccionario) o None si no existe."""
    return consultar_uno("SELECT * FROM usuarios WHERE email = %s", (email,))


def crear(nombre, email, password):
    """Guarda un usuario nuevo con la contraseña cifrada. Devuelve su id."""
    password_hash = generate_password_hash(password)
    return ejecutar(
        "INSERT INTO usuarios (nombre, email, password_hash) VALUES (%s, %s, %s)",
        (nombre, email, password_hash),
    )


def password_correcta(usuario, password):
    """Comprueba la contraseña escrita contra el hash guardado."""
    if usuario is None or usuario["password_hash"] is None:
        return False
    return check_password_hash(usuario["password_hash"], password)



def buscar_por_id(usuario_id):
    """Devuelve el usuario con ese id o None si no existe."""
    return consultar_uno("SELECT * FROM usuarios WHERE id = %s", (usuario_id,))