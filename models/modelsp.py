from flask_login import UserMixin
from Conexion.conexion import obtener_conexion
from werkzeug.security import check_password_hash
class Producto:
    def __init__(self, id_producto, nombre, precio, stock):
        self.id_producto = id_producto
        self.nombre = nombre
        self.precio = precio
        self.stock = stock

    @staticmethod
    def obtener_todos():
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()
        cursor.close()
        conexion.close()
        return productos

    @staticmethod
    def insertar(nombre, precio, stock):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO productos (nombre, precio, stock) VALUES (%s, %s, %s)", (nombre, precio, stock))
        conexion.commit()
        cursor.close()
        conexion.close()

    @staticmethod
    def obtener_por_id(id_producto):
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM productos WHERE id_producto = %s", (id_producto,))
        producto = cursor.fetchone()
        cursor.close()
        conexion.close()
        return producto

    @staticmethod
    def actualizar(id_producto, nombre, precio, stock):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("UPDATE productos SET nombre=%s, precio=%s, stock=%s WHERE id_producto=%s",
                       (nombre, precio, stock, id_producto))
        conexion.commit()
        cursor.close()
        conexion.close()

    @staticmethod
    def eliminar(id_producto):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM productos WHERE id_producto = %s", (id_producto,))
        conexion.commit()
        cursor.close()
        conexion.close()