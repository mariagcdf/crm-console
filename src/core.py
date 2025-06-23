from db import conectar
from datetime import date
import uuid

def registrar_usuario():
    print("=== REGISTRO DE USUARIO ===")
    nombre = input("Nombre: ")
    apellidos = input("Apellidos: ")
    email = input("Email: ")
    telefono = input("Teléfono (opcional): ")
    direccion = input("Dirección (opcional): ")

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
    print("Crear factura")

def mostrar_facturas_usuario():
    print("Mostrar facturas de un usuario")

def resumen_financiero():
    print("Resumen financiero")
