from db import conectar
from datetime import date
import uuid

def registrar_usuario():
    import re

def registrar_usuario():
    print("=== REGISTRO DE USUARIO ===")
    
    nombre = input("Nombre: ").strip()
    if not nombre:
        print("El nombre es obligatorio.")
        return

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
        cursor.execute('''
            INSERT INTO usuarios (id, nombre, apellidos, email, telefono, direccion, fecha_registro)
            VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (usuario_id, nombre, apellidos, email, telefono, direccion, fecha))
        conn.commit()
        print(f"Usuario registrado correctamente. ID: {usuario_id}")
    except Exception as e:
        print("Error al registrar usuario:", e)
    finally:
        conn.close()


def buscar_usuario():
    email = input("Introduce el email del usuario: ")
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
    usuario = cursor.fetchone()
    conn.close()

    if usuario:
        print(f"ID: {usuario[0]}, Nombre: {usuario[1]} {usuario[2]}, Email: {usuario[3]}")
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
    email = input("Email del usuario: ")

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM usuarios WHERE email = ?", (email,))
    fila = cursor.fetchone()

    if not fila:
        print("Usuario no encontrado.")
        conn.close()
        return

    usuario_id = fila[0]
    concepto = input("Concepto: ")
    try:
        cantidad = float(input("Cantidad (€): "))
    except ValueError:
        print("Cantidad inválida.")
        conn.close()
        return

    factura_id = "FAC" + uuid.uuid4().hex[:6].upper()
    fecha = date.today().isoformat()

    try:
        cursor.execute('''
        INSERT INTO facturas (id, usuario_id, concepto, cantidad, fecha)
        VALUES (?, ?, ?, ?, ?)''',
        (factura_id, usuario_id, concepto, cantidad, fecha))
        conn.commit()
        print(f"Factura creada correctamente. ID: {factura_id}")
    except Exception as e:
        print("Error al crear factura:", e)
    finally:
        conn.close()

def mostrar_facturas_usuario():
    print("=== FACTURAS DE UN USUARIO ===")
    email = input("Introduce el email del usuario: ")

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
        SELECT concepto, cantidad, fecha
        FROM facturas
        WHERE usuario_id = ?
        ORDER BY fecha DESC
    ''', (usuario_id,))
    facturas = cursor.fetchall()

    if not facturas:
        print("Este usuario no tiene facturas registradas.")
    else:
        for concepto, cantidad, fecha in facturas:
            print(f"- {fecha}: {concepto} — {cantidad:.2f} €")

    conn.close()

def resumen_financiero():
    print("=== RESUMEN FINANCIERO ===")
    email = input("Introduce el email del usuario: ")

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
        SELECT SUM(cantidad) FROM facturas
        WHERE usuario_id = ?
    ''', (usuario_id,))
    total = cursor.fetchone()[0]

    if total is None:
        print("Este usuario no tiene facturas registradas.")
    else:
        print(f"Total facturado: {total:.2f} €")

    conn.close()

