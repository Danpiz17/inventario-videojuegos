"""Menú interactivo del sistema de inventario de videojuegos."""
from base_datos import BaseDatos
from producto_dao import ProductoDAO
from producto_servicio import ProductoServicio, ErrorNegocio


def pedir_texto(mensaje):
    return input(mensaje).strip()


def pedir_entero(mensaje):
    try:
        return int(input(mensaje).strip())
    except ValueError:
        raise ErrorNegocio("Debe ingresar un número entero válido.")


def pedir_precio(mensaje):
    try:
        return float(input(mensaje).strip().replace(",", "."))
    except ValueError:
        raise ErrorNegocio("Debe ingresar un precio numérico válido.")


def mostrar_menu():
    print("\n===== INVENTARIO DE VIDEOJUEGOS =====")
    print("1. Registrar videojuego")
    print("2. Mostrar inventario")
    print("3. Buscar videojuego")
    print("4. Actualizar videojuego")
    print("5. Eliminar videojuego")
    print("6. Vender unidades")
    print("7. Salir")


def registrar(servicio):
    nombre = pedir_texto("Nombre: ")
    precio = pedir_precio("Precio: ")
    stock = pedir_entero("Cantidad disponible: ")
    producto = servicio.registrar(nombre, precio, stock)
    print(f"Producto guardado correctamente con ID {producto.id}.")


def mostrar_inventario(servicio):
    productos = servicio.listar()
    if not productos:
        print("El inventario está vacío.")
        return
    for producto in productos:
        print(producto)


def buscar(servicio):
    id_producto = pedir_entero("ID a buscar: ")
    print(servicio.buscar(id_producto))


def actualizar(servicio):
    id_producto = pedir_entero("ID a actualizar: ")
    servicio.buscar(id_producto)  # falla pronto si no existe
    nombre = pedir_texto("Nuevo nombre: ")
    precio = pedir_precio("Nuevo precio: ")
    stock = pedir_entero("Nuevo stock: ")
    servicio.actualizar(id_producto, nombre, precio, stock)
    print("Producto actualizado correctamente.")


def eliminar(servicio):
    id_producto = pedir_entero("ID a eliminar: ")
    servicio.eliminar(id_producto)
    print("Producto eliminado correctamente.")


def vender(servicio):
    id_producto = pedir_entero("ID del videojuego: ")
    cantidad = pedir_entero("Cantidad a vender: ")
    producto = servicio.vender(id_producto, cantidad)
    print(f"Venta realizada. Stock actual de {producto.nombre}: {producto.stock}")


def main():
    servicio = ProductoServicio(ProductoDAO(BaseDatos()))
    acciones = {
        "1": registrar, "2": mostrar_inventario, "3": buscar,
        "4": actualizar, "5": eliminar, "6": vender,
    }
    while True:
        mostrar_menu()
        try:
            opcion = input("Seleccione una opción: ").strip()
            if opcion == "7":
                print("Aplicación finalizada. ¡Hasta pronto!")
                break
            accion = acciones.get(opcion)
            if accion is None:
                print("Opción no válida. Elija un número del 1 al 7.")
                continue
            accion(servicio)
        except ErrorNegocio as error:
            print(f"Operación rechazada: {error}")
        except (KeyboardInterrupt, EOFError):
            print("\nAplicación finalizada.")
            break
        except Exception as error:  # evita cierres inesperados
            print(f"Ocurrió un error inesperado: {error}")


if __name__ == "__main__":
    main()
