from flask_login import UserMixin
from Conexion.conexion import obtener_conexion
from werkzeug.security import check_password_hash

class Usuario(UserMixin):
    def __init__(self, idusuarios, nombre, email, password):
        self.id = idusuarios
        self.nombre = nombre
        self.email = email
        self.password = password

    @staticmethod
    def obtener_por_email(email):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT idusuarios, nombre, email, password FROM usuaarios WHERE email = %s", (email,))
        fila = cursor.fetchone()
        if fila:
            return Usuario(*fila)
        return None

    @staticmethod
    def obtener_por_id(idusuarios):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT idusuarios, nombre, email, password FROM usuaarios WHERE idusuarios = %s", (idusuarios,))
        fila = cursor.fetchone()
        if fila:
            return Usuario(*fila)
        return None

    def verificar_password(self, password_plano):
        return check_password_hash(self.password, password_plano)


class User:
    pass