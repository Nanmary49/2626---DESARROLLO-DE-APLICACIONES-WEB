# ================================================================
# models.py — Narvi Collector Scale Models
# Clase de usuario compatible con Flask-Login
# Semana 14
# ================================================================

from flask_login import UserMixin
from conexion.conexion import get_db


class Usuario(UserMixin):
    """
    Clase de usuario compatible con Flask-Login.
    Hereda de UserMixin para obtener los métodos
    is_authenticated, is_active, is_anonymous y get_id.
    """

    def __init__(self, id, usuario, password):
        self.id       = id
        self.usuario  = usuario
        self.password = password

    @staticmethod
    def get_by_id(user_id):
        """
        Recupera un usuario desde MySQL por su ID.
        Usado por load_user() de Flask-Login.
        """
        conn   = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM usuarios WHERE id = %s', (user_id,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            return Usuario(user['id'], user['usuario'], user['password'])
        return None

    @staticmethod
    def get_by_usuario(usuario):
        """
        Recupera un usuario desde MySQL por su nombre de usuario.
        Usado durante el proceso de login.
        """
        conn   = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM usuarios WHERE usuario = %s', (usuario,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            return Usuario(user['id'], user['usuario'], user['password'])
        return None