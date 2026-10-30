"""Servicio: validaciones y reglas del negocio."""
from modelo import Producto


class ErrorNegocio(Exception):
    """Error de validación o de regla de negocio."""


class ProductoServicio:
    def __init__(self, dao):
        self.dao = dao

    # ---------- validaciones ----------
    @staticmethod
    def _validar_nombre(nombre):
        nombre = (nombre or "").strip()
        if not nombre:
            raise ErrorNegocio("El nombre no puede estar vacío.")
        return nombre

    @staticmethod
    def _validar_precio(precio):
        if precio <= 0:
            raise ErrorNegocio("El precio debe ser mayor que cero.")
        return precio

    @staticmethod
    def _validar_stock(stock):
        if stock < 0:
            raise ErrorNegocio("La cantidad en inventario no puede ser negativa.")
        return stock

    def _obtener_existente(self, id_producto):
        producto = self.dao.buscar_por_id(id_producto)
        if producto is None:
            raise ErrorNegocio(f"No existe un videojuego con ID {id_producto}.")
        return producto

    # ---------- operaciones ----------
    def registrar(self, nombre, precio, stock):
        producto = Producto(
            self._validar_nombre(nombre),
            self._validar_precio(precio),
            self._validar_stock(stock),
        )
        return self.dao.insertar(producto)

    def listar(self):
        return self.dao.listar()

    def buscar(self, id_producto):
        return self._obtener_existente(id_producto)

    def actualizar(self, id_producto, nombre, precio, stock):
        producto = self._obtener_existente(id_producto)
        producto.nombre = self._validar_nombre(nombre)
        producto.precio = self._validar_precio(precio)
        producto.stock = self._validar_stock(stock)
        self.dao.actualizar(producto)
        return producto

    def eliminar(self, id_producto):
        self._obtener_existente(id_producto)
        self.dao.eliminar(id_producto)

    def vender(self, id_producto, cantidad):
        producto = self._obtener_existente(id_producto)
        if cantidad <= 0:
            raise ErrorNegocio("La cantidad a vender debe ser mayor que cero.")
        if cantidad > producto.stock:
            raise ErrorNegocio(
                f"Stock insuficiente: disponibles {producto.stock}, solicitados {cantidad}."
            )
        producto.stock -= cantidad
        self.dao.actualizar_stock(id_producto, producto.stock)
        return producto
