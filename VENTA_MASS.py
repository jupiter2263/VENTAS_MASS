from datetime import datetime

def registrar_productos():
    productos = []
    total_compra = 0

    while True:
        print("\n--- REGISTRO DE PRODUCTOS ---")
        nombre = input("Ingrese el nombre del producto: ").strip()

        while not nombre:
            print("El nombre no puede estar vacío.")
            nombre = input("Ingrese el nombre del producto: ").strip()

        while True:
            try:
                precio = float(input("Ingrese el precio unitario (S/): "))
                if precio > 0:
                    break
                print("El precio debe ser mayor que cero.")
            except ValueError:
                print("Ingrese un precio válido.")

        while True:
            try:
                cantidad = int(input("Ingrese la cantidad: "))
                if cantidad > 0:
                    break
                print("La cantidad debe ser mayor que cero.")
            except ValueError:
                print("Ingrese una cantidad entera válida.")

        subtotal = precio * cantidad
        total_compra += subtotal

        productos.append({
            "nombre": nombre,
            "precio": precio,
            "cantidad": cantidad,
            "subtotal": subtotal
        })

        print(f"Subtotal: S/ {subtotal:.2f}")
        print(f"Total acumulado: S/ {total_compra:.2f}")

        while True:
            respuesta = input("¿Desea agregar otro producto? (S/N): ").strip().upper()
            if respuesta in ("S", "N"):
                break
            print("Ingrese S para sí o N para no.")

        if respuesta == "N":
            break

    return productos, total_compra


def validar_pago(total_compra):
    while True:
        try:
            dinero = float(input("\nIngrese el dinero recibido (S/): "))

            if dinero < 0:
                print("El dinero no puede ser negativo.")
            elif dinero < total_compra:
                faltante = total_compra - dinero
                print(f"Dinero insuficiente. Falta S/ {faltante:.2f}")
            else:
                return dinero

        except ValueError:
            print("Ingrese un monto válido.")


def guardar_venta(productos, total_compra, dinero, vuelto):
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    with open("historial_ventas.txt", "a", encoding="utf-8") as archivo:
        archivo.write("\n====================================\n")
        archivo.write("SISTEMA DE VENTAS MASS\n")
        archivo.write(f"Fecha: {fecha}\n")
        archivo.write("------------------------------------\n")

        for producto in productos:
            archivo.write(
                f"Producto: {producto['nombre']} | "
                f"Precio: S/ {producto['precio']:.2f} | "
                f"Cantidad: {producto['cantidad']} | "
                f"Subtotal: S/ {producto['subtotal']:.2f}\n"
            )

        archivo.write("------------------------------------\n")
        archivo.write(f"Total: S/ {total_compra:.2f}\n")
        archivo.write(f"Dinero recibido: S/ {dinero:.2f}\n")
        archivo.write(f"Vuelto: S/ {vuelto:.2f}\n")
        archivo.write("====================================\n")


def mostrar_resumen(productos, total_compra, dinero, vuelto):
    print("\n========== COMPROBANTE DE VENTA ==========")

    for producto in productos:
        print(
            f"{producto['nombre']} | "
            f"{producto['cantidad']} x S/ {producto['precio']:.2f} "
            f"= S/ {producto['subtotal']:.2f}"
        )

    print("------------------------------------------")
    print(f"Total de la compra: S/ {total_compra:.2f}")
    print(f"Dinero recibido:    S/ {dinero:.2f}")
    print(f"Vuelto:             S/ {vuelto:.2f}")
    print("==========================================")


def main():
    print("====================================")
    print("       SISTEMA DE VENTAS MASS")
    print("====================================")

    productos, total_compra = registrar_productos()
    dinero = validar_pago(total_compra)
    vuelto = dinero - total_compra

    mostrar_resumen(productos, total_compra, dinero, vuelto)

    try:
        guardar_venta(productos, total_compra, dinero, vuelto)
        print("\nLa venta se guardó en historial_ventas.txt.")
    except OSError:
        print("\nNo se pudo guardar la venta en el archivo.")

    print("Fin del proceso.")


if __name__ == "__main__":
    main()
