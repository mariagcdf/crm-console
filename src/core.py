from db import conectar
from datetime import date
import uuid
import re

def registrar_usuario():
    print("=== REGISTRO DE USUARIO ===")

    while True:
        nombre = input("Nombre: ").strip()
        if nombre:  # nombre correcto → seguimos
            break
        print("El nombre es obligatorio.")
        reintentar = input("¿Quieres volver a introducir un nombre? (s/n): ").strip().lower()
        if reintentar != "s":  # cualquier cosa distinta de “s” cancela el registro
            print("Registro cancelado.")
            return  # volvemos al menú principal

    apellidos = input("Apellidos: ").strip()
    if not apellidos:
        print("Al menos un apellido es obligatorio.")
        return

    email = input("Email: ").strip()
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        print("Email no válido.")
        return

    telefono = input("Teléfono (opcional): ").strip()
    direccion = input("Dirección (opcional): ").strip()

    usuario_id = "USR" + uuid.uuid4().hex[:6].upper()
    fecha = date.today().isoformat()

    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO usuarios (id, nombre, apellidos, email, telefono, direccion, fecha_registro) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (usuario_id, nombre, apellidos, email, telefono, direccion, fecha)
        )
        conn.commit()
        print(f"Usuario registrado correctamente. ID: {usuario_id}")
    except Exception as e:
        print("Error al registrar usuario:", e)
    finally:
        conn.close()


def buscar_usuario():
    email = input("Introduce el email del usuario: ").strip()

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
    usuario = cursor.fetchone()
    conn.close()

    if usuario:
        print("\n=== DATOS DEL USUARIO ===")
        print(f"ID: {usuario[0]}")
        print(f"Nombre: {usuario[1]} {usuario[2]}")
        print(f"Email: {usuario[3]}")
        print(f"Teléfono: {usuario[4] if usuario[4] else 'No disponible'}")
        print(f"Dirección: {usuario[5] if usuario[5] else 'No disponible'}")
        print(f"Fecha de registro: {usuario[6]}")
    else:
        print("Usuario no encontrado.")

def mostrar_usuarios():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, apellidos, email FROM usuarios")
    usuarios = cursor.fetchall()
    conn.close()

    print("=== LISTA DE USUARIOS ===")
    for u in usuarios:
        print(f"{u[0]} - {u[1]} {u[2]} - {u[3]}")

def crear_factura():
    print("=== CREAR FACTURA ===")
    email = input("Email del usuario: ").strip()

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM usuarios WHERE email = ?", (email,))
    fila = cursor.fetchone()

    if not fila:
        print("Usuario no encontrado.")
        conn.close()
        return

    usuario_id = fila[0]
    descripcion = input("Descripción (concepto): ").strip()
    try:
        monto = float(input("Monto (€): "))
    except ValueError:
        print("Monto inválido.")
        conn.close()
        return

    estado = input("Estado [Pendiente/Pagada/Cancelada]: ").strip().capitalize()
    if estado not in ['Pendiente', 'Pagada', 'Cancelada']:
        print("Estado no válido.")
        conn.close()
        return

    numero = "FAC" + uuid.uuid4().hex[:6].upper()
    fecha_emision = date.today().isoformat()

    try:
        cursor.execute('''
            INSERT INTO facturas (numero, usuario_id, fecha_emision, descripcion, monto, estado)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (numero, usuario_id, fecha_emision, descripcion, monto, estado))
        conn.commit()
        print(f"Factura creada correctamente. Número: {numero}")
    except Exception as e:
        print("Error al crear factura:", e)
    finally:
        conn.close()


def mostrar_facturas_usuario():
    print("=== FACTURAS DE UN USUARIO ===")
    email = input("Introduce el email del usuario: ").strip()

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM usuarios WHERE email = ?", (email,))
    fila = cursor.fetchone()
    if not fila:
        print("Usuario no encontrado.")
        conn.close()
        return

    usuario_id = fila[0]

    cursor.execute('''
        SELECT numero, fecha_emision, descripcion, monto, estado
        FROM facturas
        WHERE usuario_id = ?
        ORDER BY fecha_emision DESC
    ''', (usuario_id,))
    facturas = cursor.fetchall()

    if not facturas:
        print("Este usuario no tiene facturas registradas.")
    else:
        print("\nFACTURAS:")
        for numero, fecha, descripcion, monto, estado in facturas:
            print(f"- [{estado}] {fecha} | Nº {numero} | {descripcion} — {monto:.2f} €")

    conn.close()


def resumen_financiero():
    print("=== RESUMEN FINANCIERO ===")
    email = input("Introduce el email del usuario: ").strip()

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM usuarios WHERE email = ?", (email,))
    fila = cursor.fetchone()
    if not fila:
        print("Usuario no encontrado.")
        conn.close()
        return

    usuario_id = fila[0]

    cursor.execute('''
        SELECT estado, COUNT(*), SUM(monto)
        FROM facturas
        WHERE usuario_id = ?
        GROUP BY estado
    ''', (usuario_id,))
    totales = cursor.fetchall()

    if not totales:
        print("Este usuario no tiene facturas registradas.")
    else:
        print("\nResumen por estado:")
        total_pagado = 0
        for estado, cantidad, monto in totales:
            print(f"- {estado} ({cantidad}): {monto:.2f} €")
            if estado == "Pagada":
                total_pagado += monto

        print(f"\nTotal general facturado (solo pagadas): {total_pagado:.2f} €")

    conn.close()




def modificar_usuario():
    print("=== MODIFICAR USUARIO ===")
    email = input("Email actual del usuario: ")

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
    usuario = cursor.fetchone()

    if not usuario:
        print("Usuario no encontrado.")
        conn.close()
        return

    print(f"Usuario encontrado: {usuario[1]} {usuario[2]}")

    nuevo_email = input("Nuevo email (dejar en blanco para no cambiar): ")
    nuevo_telefono = input("Nuevo teléfono (dejar en blanco para no cambiar): ")
    nueva_direccion = input("Nueva dirección (dejar en blanco para no cambiar): ")

    if nuevo_email:
        cursor.execute("UPDATE usuarios SET email = ? WHERE id = ?", (nuevo_email, usuario[0]))
    if nuevo_telefono:
        cursor.execute("UPDATE usuarios SET telefono = ? WHERE id = ?", (nuevo_telefono, usuario[0]))
    if nueva_direccion:
        cursor.execute("UPDATE usuarios SET direccion = ? WHERE id = ?", (nueva_direccion, usuario[0]))

    conn.commit()
    conn.close()
    print("Usuario actualizado correctamente.")


def eliminar_usuario():
    print("=== ELIMINAR USUARIO ===")
    email = input("Email del usuario a eliminar: ").strip()

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM usuarios WHERE email = ?", (email,))
    resultado = cursor.fetchone()

    if resultado:
        usuario_id = resultado[0]

        # Eliminar facturas asociadas primero por restricción de clave externa
        cursor.execute("DELETE FROM facturas WHERE usuario_id = ?", (usuario_id,))
        cursor.execute("DELETE FROM usuarios WHERE id = ?", (usuario_id,))
        conn.commit()
        print("Usuario y facturas eliminadas correctamente.")
    else:
        print("No se encontró ningún usuario con ese email.")

    conn.close()

