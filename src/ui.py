from core import registrar_usuario, buscar_usuario, crear_factura, mostrar_usuarios, mostrar_facturas_usuario, resumen_financiero

def mostrar_menu():
    while True:
        print("\n=== SISTEMA CRM ===")
        print("1. Registrar nuevo usuario")
        print("2. Buscar usuario")
        print("3. Crear factura para usuario")
        print("4. Mostrar todos los usuarios")
        print("5. Mostrar facturas de un usuario")
        print("6. Resumen financiero por usuario")
        print("7. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_usuario()
        elif opcion == "2":
            buscar_usuario()
        elif opcion == "3":
            crear_factura()
        elif opcion == "4":
            mostrar_usuarios()
        elif opcion == "5":
            mostrar_facturas_usuario()
        elif opcion == "6":
            resumen_financiero()
        elif opcion == "7":
            print("Saliendo...")
            break
        else:
            print("Opción inválida.")
