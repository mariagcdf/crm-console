from core import modificar_factura, registrar_usuario, buscar_usuario, crear_factura, mostrar_usuarios, mostrar_facturas_usuario, resumen_financiero, modificar_usuario, eliminar_usuario

def mostrar_menu():
    continuar = True
    while continuar:
        print("\n=== SISTEMA CRM ===")
        print("1. Registrar nuevo usuario")
        print("2. Buscar usuario")
        print("3. Crear factura para usuario")
        print("4. Editar factura")
        print("5. Mostrar todos los usuarios")
        print("6. Mostrar facturas de un usuario")
        print("7. Resumen financiero por usuario")
        print("8. Modificar datos de un usuario")
        print("9. Eliminar un usuario")
        print("10. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_usuario()
        elif opcion == "2":
            buscar_usuario()
        elif opcion == "3":
            crear_factura()
        elif opcion == "4":
            modificar_factura()
        elif opcion == "5":
            mostrar_usuarios()
        elif opcion == "6":
            mostrar_facturas_usuario()
        elif opcion == "7":
            resumen_financiero()
        elif opcion == "8":
            modificar_usuario()
        elif opcion == "9":
            eliminar_usuario()
        elif opcion == "10":
            print("Saliendo del sistema CRM.")
            break
        else:
            print("Opción no válida.")
            continue

        seguir = input("\n¿Desea realizar otra operación? (s/n): ").lower()
        if seguir != 's':
            continuar = False
