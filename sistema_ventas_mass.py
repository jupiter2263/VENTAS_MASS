import json
import os
from datetime import datetime

ARCHIVO_PRODUCTOS = "catalogo_productos.json"
ARCHIVO_VENTAS = "historial_ventas.txt"


def cargar_productos():
    """Carga el catálogo desde un archivo. Si no existe, crea uno inicial."""
    if not os.path.exists(ARCHIVO_PRODUCTOS):
        productos_iniciales = [
            {"codigo": "P001", "nombre": "Gaseosa", "precio": 5.00},
            {"codigo": "P002", "nombre": "Galletas", "precio": 2.50},
            {"codigo": "P003", "nombre": "Leche", "precio": 4.50},
            {"codigo": "P004", "nombre": "Arroz", "precio": 4.00},
            {"codigo": "P005", "nombre": "Aceite", "precio": 8.50},
        ]
        guardar_productos(productos_iniciales)
        return productos_iniciales

    try:
        with open(ARCHIVO_PRODUCTOS, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except (json.JSONDecodeError, OSError):
        print("No se pudo leer el catálogo. Se iniciará con una lista vacía.")
        return []


def guardar_productos(productos):
    """Guarda el catálogo en un archivo de texto JSON."""
    with open(ARCHIVO_PRODUCTOS, "w", encoding="utf-8") as archivo:
        json.dump(productos, archivo, ensure_ascii=False, indent=4)


def siguiente_codigo(productos):
    """Genera el siguiente código disponible: P001, P002, etc."""
    mayor = 0
    for producto in productos:
        codigo = producto.get("codigo", "")
        if codigo.startswith("P") and codigo[1:].isdigit():
            mayor = max(mayor, int(codigo[1:]))
    return f"P{mayor + 1:03d}"


def agregar_producto(productos):
    print("\n--- AGREGAR PRODUCTO ---")
    nombre = input("Nombre del producto: ").strip()

    if not nombre:
        print("El nombre no puede estar vacío.")
        return

    if any(p["nombre"].casefold() == nombre.casefold() for p in productos):
        print("Ya existe un producto con ese nombre.")
        return

    try:
        precio = float(input("Precio unitario (S/): "))
        if precio <= 0:
            print("El precio debe ser mayor que cero.")
            return
    except ValueError:
        print("Ingresa un precio válido.")
        return

    producto = {
        "codigo": siguiente_codigo(productos),
        "nombre": nombre,
        "precio": round(precio, 2)
    }
    productos.append(producto)
    guardar_productos(productos)

    print(f"Producto agregado correctamente. Código asignado: {producto['codigo']}")


def mostrar_productos(productos):
    print("\n--- CATÁLOGO DE PRODUCTOS ---")
    if not productos:
        print("Todavía no hay productos registrados.")
        return

    print(f"{'Código':<10}{'Producto':<25}{'Precio':>12}")
    print("-" * 47)
    for producto in productos:
        print(
            f"{producto['codigo']:<10}"
            f"{producto['nombre']:<25}"
            f"S/ {producto['precio']:>8.2f}"
        )


def registrar_venta(productos):
    if not productos:
        print("\nNo hay productos en el catálogo. Agrega un producto primero.")
        return

    carrito = []
    print("\n--- REGISTRAR VENTA ---")
    mostrar_productos(productos)

    while True:
        codigo = input(
            "\nIngresa el código del producto (o escribe FIN para terminar): "
        ).strip().upper()

        if codigo == "FIN":
            break

        producto = next(
            (p for p in productos if p["codigo"].upper() == codigo),
            None
        )

        if producto is None:
            print("Código no encontrado. Inténtalo nuevamente.")
            continue

        try:
            cantidad = int(input(f"Cantidad de {producto['nombre']}: "))
            if cantidad <= 0:
                print("La cantidad debe ser mayor que cero.")
                continue
        except ValueError:
            print("Ingresa una cantidad entera válida.")
            continue

        subtotal = round(producto["precio"] * cantidad, 2)
        carrito.append({
            "codigo": producto["codigo"],
            "nombre": producto["nombre"],
            "precio": producto["precio"],
            "cantidad": cantidad,
            "subtotal": subtotal
        })
        print(f"Agregado: {producto['nombre']} x {cantidad} = S/ {subtotal:.2f}")

        continuar = input("¿Deseas agregar otro producto? (S/N): ").strip().upper()
        if continuar != "S":
            break

    if not carrito:
        print("No se registraron productos en esta venta.")
        return

    total = round(sum(item["subtotal"] for item in carrito), 2)

    print("\n--- RESUMEN DE COMPRA ---")
    for item in carrito:
        print(
            f"{item['nombre']} x {item['cantidad']} "
            f"- S/ {item['subtotal']:.2f}"
        )
    print(f"TOTAL A PAGAR: S/ {total:.2f}")

    while True:
        try:
            pago = float(input("Dinero recibido (S/): "))
            if pago < total:
                print(f"Dinero insuficiente. Faltan S/ {total - pago:.2f}.")
                continue
            if pago < 0:
                print("El pago no puede ser negativo.")
                continue
            break
        except ValueError:
            print("Ingresa un monto válido.")

    vuelto = round(pago - total, 2)
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    print(f"Dinero recibido: S/ {pago:.2f}")
    print(f"Vuelto: S/ {vuelto:.2f}")

    # Guarda el detalle de la venta para conservar el historial.
    with open(ARCHIVO_VENTAS, "a", encoding="utf-8") as archivo:
        archivo.write("\n" + "=" * 45 + "\n")
        archivo.write(f"VENTA - {fecha}\n")
        for item in carrito:
            archivo.write(
                f"{item['codigo']} | {item['nombre']} | "
                f"{item['cantidad']} x S/ {item['precio']:.2f} "
                f"= S/ {item['subtotal']:.2f}\n"
            )
        archivo.write(f"TOTAL: S/ {total:.2f}\n")
        archivo.write(f"PAGO: S/ {pago:.2f}\n")
        archivo.write(f"VUELTO: S/ {vuelto:.2f}\n")

    print("Venta registrada y guardada correctamente.")


def ver_historial():
    print("\n--- HISTORIAL DE VENTAS ---")
    if not os.path.exists(ARCHIVO_VENTAS):
        print("Todavía no hay ventas registradas.")
        return

    with open(ARCHIVO_VENTAS, "r", encoding="utf-8") as archivo:
        contenido = archivo.read()

    if contenido.strip():
        print(contenido)
    else:
        print("Todavía no hay ventas registradas.")


def menu():
    productos = cargar_productos()

    while True:
        print("\n========== SISTEMA DE VENTAS MASS ==========")
        print("1. Registrar una venta")
        print("2. Agregar un producto al catálogo")
        print("3. Ver catálogo de productos")
        print("4. Ver historial de ventas")
        print("5. Salir")

        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            registrar_venta(productos)
        elif opcion == "2":
            agregar_producto(productos)
        elif opcion == "3":
            mostrar_productos(productos)
        elif opcion == "4":
            ver_historial()
        elif opcion == "5":
            print("Gracias por utilizar el sistema de ventas.")
            break
        else:
            print("Opción no válida. Selecciona del 1 al 5.")


if __name__ == "__main__":
    menu()
