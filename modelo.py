"""Modelo de datos del sistema de inventario."""


class Producto:
    """Representa un videojuego del inventario."""

    def __init__(self, nombre, precio, stock, id=None):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.stock = stock

    def __str__(self):
        return (f"ID: {self.id:<4} | {self.nombre:<30} | "
                f"Precio: ${self.precio:>12,.0f} | Stock: {self.stock}")
