"""Ejecuta los casos de prueba del taller sobre una base temporal."""
import os
import tempfile
from base_datos import BaseDatos
from producto_dao import ProductoDAO
from producto_servicio import ProductoServicio, ErrorNegocio

ruta = os.path.join(tempfile.mkdtemp(), "prueba.db")
s = ProductoServicio(ProductoDAO(BaseDatos(ruta)))


def caso(titulo):
    print(f"\n--- {titulo} ---")


caso("1. Registrar Resident Evil 4 (precio 180000, stock 10)")
re4 = s.registrar("Resident Evil 4", 180000, 10)
s.registrar("God of War", 150000, 5)
print(f"Producto guardado correctamente (ID {re4.id})")

caso("2. Mostrar inventario")
for p in s.listar():
    print(p)

caso("3. Buscar un ID existente")
print(s.buscar(re4.id))

caso("4. Actualizar un producto (persistido en SQLite)")
s.actualizar(2, "God of War Ragnarok", 200000, 8)
s2 = ProductoServicio(ProductoDAO(BaseDatos(ruta)))  # nueva conexión
print(s2.buscar(2))

caso("5. Vender 3 unidades de Resident Evil 4 (stock 10 -> 7)")
print("Stock antes:", s.buscar(re4.id).stock)
s.vender(re4.id, 3)
print("Stock después:", s.buscar(re4.id).stock)

caso("6. Intentar vender 20 unidades")
try:
    s.vender(re4.id, 20)
except ErrorNegocio as e:
    print("Operación rechazada:", e)
print("Stock conservado:", s.buscar(re4.id).stock)

caso("7. Buscar un ID inexistente")
try:
    s.buscar(999)
except ErrorNegocio as e:
    print("Operación rechazada:", e)

caso("8. Eliminar un producto")
s.eliminar(2)
for p in s.listar():
    print(p)

caso("Validaciones adicionales")
for desc, fn in [
    ("nombre vacío", lambda: s.registrar("  ", 100, 1)),
    ("precio 0", lambda: s.registrar("X", 0, 1)),
    ("stock negativo", lambda: s.registrar("X", 100, -1)),
    ("venta de 0 unidades", lambda: s.vender(re4.id, 0)),
]:
    try:
        fn()
    except ErrorNegocio as e:
        print(f"{desc}: rechazado -> {e}")
