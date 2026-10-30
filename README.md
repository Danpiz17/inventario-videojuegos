# Sistema de Inventario de Videojuegos

## Propósito
Aplicación de consola en Python que administra el inventario de una tienda de videojuegos (CRUD y ventas), guardando la información en **SQLite** y aplicando el **patrón DAO** con separación de responsabilidades.

## Estructura
| Archivo | Responsabilidad |
|---|---|
| `modelo.py` | Clase `Producto` (id, nombre, precio, stock). |
| `base_datos.py` | Conexión a SQLite y creación de la tabla `productos`. |
| `producto_dao.py` | Todas las consultas SQL (insertar, listar, buscar, actualizar, eliminar). |
| `producto_servicio.py` | Validaciones y reglas de negocio (`ErrorNegocio`). |
| `main.py` | Menú interactivo; solo usa el servicio, sin SQL. |
| `pruebas.py` | Script que ejecuta los casos de prueba del taller. |

La base `inventario.db` se crea automáticamente en la primera ejecución y **conserva los datos entre ejecuciones**. Ya no se registra el videojuego de ejemplo al iniciar.

## Funcionalidades
1. Registrar videojuego (nombre, precio, cantidad).
2. Mostrar inventario (ID, nombre, precio, stock).
3. Buscar videojuego por ID (informa si no existe).
4. Actualizar nombre, precio y stock.
5. Eliminar por ID.
6. Vender unidades (descuenta del inventario).
7. Salir.

### Validaciones
- Nombre no vacío.
- Precio mayor que cero.
- Stock no negativo.
- Venta de cantidad mayor que cero y no superior al stock disponible.
- Mensaje claro cuando el ID no existe.
- Las entradas no numéricas se capturan y no cierran el programa.

## Cómo ejecutarlo
Requiere Python 3.8+ (SQLite viene incluido, no hay que instalar nada).

```bash
python main.py      # abre el menú interactivo
python pruebas.py   # ejecuta los casos de prueba
```

## Evidencias de pruebas
Salida real de `python pruebas.py`:

```text

--- 1. Registrar Resident Evil 4 (precio 180000, stock 10) ---
Producto guardado correctamente (ID 1)

--- 2. Mostrar inventario ---
ID: 1    | Resident Evil 4                | Precio: $     180,000 | Stock: 10
ID: 2    | God of War                     | Precio: $     150,000 | Stock: 5

--- 3. Buscar un ID existente ---
ID: 1    | Resident Evil 4                | Precio: $     180,000 | Stock: 10

--- 4. Actualizar un producto (persistido en SQLite) ---
ID: 2    | God of War Ragnarok            | Precio: $     200,000 | Stock: 8

--- 5. Vender 3 unidades de Resident Evil 4 (stock 10 -> 7) ---
Stock antes: 10
Stock después: 7

--- 6. Intentar vender 20 unidades ---
Operación rechazada: Stock insuficiente: disponibles 7, solicitados 20.
Stock conservado: 7

--- 7. Buscar un ID inexistente ---
Operación rechazada: No existe un videojuego con ID 999.

--- 8. Eliminar un producto ---
ID: 1    | Resident Evil 4                | Precio: $     180,000 | Stock: 7

--- Validaciones adicionales ---
nombre vacío: rechazado -> El nombre no puede estar vacío.
precio 0: rechazado -> El precio debe ser mayor que cero.
stock negativo: rechazado -> La cantidad en inventario no puede ser negativa.
venta de 0 unidades: rechazado -> La cantidad a vender debe ser mayor que cero.
```

Operación exitosa: venta de 3 unidades (stock 10 → 7). Operación rechazada: venta de 20 unidades con stock 7.

Las capturas de pantalla de las operaciones CRUD y de las validaciones se entregan en el documento Word de evidencias.
