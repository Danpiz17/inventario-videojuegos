"""DAO: único lugar donde se escriben las consultas SQL."""
from modelo import Producto


class ProductoDAO:
    def __init__(self, base_datos):
        self.bd = base_datos

    @staticmethod
    def _a_producto(fila):
        return Producto(id=fila[0], nombre=fila[1], precio=fila[2], stock=fila[3])

    def insertar(self, producto):
        conexion = self.bd.conectar()
        try:
            with conexion:
                cursor = conexion.execute(
                    "INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)",
                    (producto.nombre, producto.precio, producto.stock),
                )
            producto.id = cursor.lastrowid
            return producto
        finally:
            conexion.close()

    def listar(self):
        conexion = self.bd.conectar()
        try:
            filas = conexion.execute(
                "SELECT id, nombre, precio, stock FROM productos ORDER BY id"
            ).fetchall()
            return [self._a_producto(f) for f in filas]
        finally:
            conexion.close()

    def buscar_por_id(self, id_producto):
        conexion = self.bd.conectar()
        try:
            fila = conexion.execute(
                "SELECT id, nombre, precio, stock FROM productos WHERE id = ?",
                (id_producto,),
            ).fetchone()
            return self._a_producto(fila) if fila else None
        finally:
            conexion.close()

    def actualizar(self, producto):
        """Devuelve True si se modificó alguna fila."""
        conexion = self.bd.conectar()
        try:
            with conexion:
                cursor = conexion.execute(
                    "UPDATE productos SET nombre = ?, precio = ?, stock = ? WHERE id = ?",
                    (producto.nombre, producto.precio, producto.stock, producto.id),
                )
            return cursor.rowcount > 0
        finally:
            conexion.close()

    def actualizar_stock(self, id_producto, nuevo_stock):
        conexion = self.bd.conectar()
        try:
            with conexion:
                cursor = conexion.execute(
                    "UPDATE productos SET stock = ? WHERE id = ?",
                    (nuevo_stock, id_producto),
                )
            return cursor.rowcount > 0
        finally:
            conexion.close()

    def eliminar(self, id_producto):
        """Devuelve True si se eliminó alguna fila."""
        conexion = self.bd.conectar()
        try:
            with conexion:
                cursor = conexion.execute(
                    "DELETE FROM productos WHERE id = ?", (id_producto,)
                )
            return cursor.rowcount > 0
        finally:
            conexion.close()
