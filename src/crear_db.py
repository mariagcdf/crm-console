import sqlite3
import os
import uuid
import random
from datetime import date
from faker import Faker

fake = Faker()

def conectar():
    ruta_db = os.path.join(os.path.dirname(__file__), '..', 'data', 'crm.db')
    return sqlite3.connect(ruta_db)

def generar_usuarios(n):
    usuarios = []
    for _ in range(n):
        nombre = fake.first_name()
        apellidos = fake.last_name()
        email = fake.unique.email()
        telefono = fake.phone_number()
        direccion = fake.address().replace("\n", ", ")
        usuarios.append((nombre, apellidos, email, telefono, direccion))
    return usuarios

def generar_facturas(emails, max_por_usuario=4):
    conceptos = ["Servicio mensual", "Mantenimiento", "Licencia", "Consultoría", "Renovación"]
    facturas = []
    for email in emails:
        for _ in range(random.randint(1, max_por_usuario)):
            concepto = random.choice(conceptos)
            cantidad = round(random.uniform(10.0, 200.0), 2)
            facturas.append((email, concepto, cantidad))
    return facturas

def insertar_datos():
    conn = conectar()
    cursor = conn.cursor()

    usuarios = generar_usuarios(10)

    for nombre, apellidos, email, telefono, direccion in usuarios:
        usuario_id = "USR" + uuid.uuid4().hex[:6].upper()
        fecha = date.today().isoformat()
        try:
            cursor.execute('''
                INSERT INTO usuarios (id, nombre, apellidos, email, telefono, direccion, fecha_registro)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (usuario_id, nombre, apellidos, email, telefono, direccion, fecha))
        except:
            continue

    conn.commit()

    cursor.execute("SELECT id, email FROM usuarios")
    user_map = {email: uid for uid, email in cursor.fetchall()}

    facturas = generar_facturas(list(user_map.keys()))

    for email, concepto, cantidad in facturas:
        factura_id = "FAC" + uuid.uuid4().hex[:6].upper()
        fecha = date.today().isoformat()
        try:
            cursor.execute('''
                INSERT INTO facturas (id, usuario_id, concepto, cantidad, fecha)
                VALUES (?, ?, ?, ?, ?)
            ''', (factura_id, user_map[email], concepto, cantidad, fecha))
        except:
            continue

    conn.commit()
    conn.close()
    print("Usuarios y facturas generados aleatoriamente.")

if __name__ == "__main__":
    insertar_datos()
