"""Administra la conexión y la creación de la base de datos SQLite."""
import sqlite3


class BaseDatos:
    def __init__(self, ruta="inventario.db"):
        self.ruta = ruta
        self.crear_tabla()

    def conectar(self):
        """Devuelve una nueva conexión a la base de datos."""
        return sqlite3.connect(self.ruta)

    def crear_tabla(self):
        """Crea la tabla productos si todavía no existe."""
        with self.conectar() as conexion:
            conexion.execute(
                """
                CREATE TABLE IF NOT EXISTS productos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    precio REAL NOT NULL,
                    stock INTEGER NOT NULL
                )
                """
            )
