# src/crear_db.py
"""
Script para poblar la base de datos crm.db con usuarios y facturas de ejemplo
adaptado a la estructura actual de la tabla `facturas`
(numero, usuario_id, fecha_emision, descripcion, monto, estado).
"""

import sqlite3
import os
import uuid
import random
from datetime import date
from faker import Faker

fake = Faker()

# -------------------------------------------------
# Conexión a la base de datos (se crea si no existe)
# -------------------------------------------------
def conectar():
    ruta_db = os.path.join(
        os.path.dirname(__file__),  # .../src
        "..",                       # sube a crm-console
        "data",
        "crm.db"
    )
    return sqlite3.connect(ruta_db)


# -------------------------------------------------
# Generadores de datos
# -------------------------------------------------
def generar_usuarios(n=10):
    """Devuelve una lista de tuplas con datos de usuario."""
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
    """Devuelve una lista de tuplas (email, descripcion, monto, estado)."""
    conceptos = [
        "Servicio mensual",
        "Mantenimiento",
        "Licencia",
        "Consultoría",
        "Renovación"
    ]
    estados = ["Pendiente", "Pagada", "Cancelada"]
    facturas = []
    for email in emails:
        for _ in range(random.randint(1, max_por_usuario)):
            descripcion = random.choice(conceptos)
            monto = round(random.uniform(10.0, 200.0), 2)
            estado = random.choice(estados)
            facturas.append((email, descripcion, monto, estado))
    return facturas


# -------------------------------------------------
# Inserción de datos
# -------------------------------------------------
def insertar_datos():
    conn = conectar()
    cursor = conn.cursor()

    # 1) Usuarios
    usuarios = generar_usuarios(10)
    for nombre, apellidos, email, tel, dire in usuarios:
        usuario_id = "USR" + uuid.uuid4().hex[:6].upper()
        fecha_reg = date.today().isoformat()
        try:
            cursor.execute(
                """
                INSERT INTO usuarios
                (id, nombre, apellidos, email, telefono, direccion, fecha_registro)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (usuario_id, nombre, apellidos, email, tel, dire, fecha_reg)
            )
        except sqlite3.IntegrityError:
            # Si el email ya existe, se ignora para no duplicar
            continue

    conn.commit()

    # Mapa email -> id
    cursor.execute("SELECT id, email FROM usuarios")
    user_map = {e: uid for uid, e in cursor.fetchall()}

    # 2) Facturas
    facturas = generar_facturas(list(user_map.keys()))

    for email, descripcion, monto, estado in facturas:
        numero = "FAC" + uuid.uuid4().hex[:6].upper()
        fecha_emision = date.today().isoformat()
        try:
            cursor.execute(
                """
                INSERT INTO facturas
                (numero, usuario_id, fecha_emision, descripcion, monto, estado)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (numero, user_map[email], fecha_emision, descripcion, monto, estado)
            )
        except sqlite3.IntegrityError:
            # Evita duplicar número de factura
            continue

    conn.commit()
    conn.close()
    print("Usuarios y facturas generados aleatoriamente.")


# -------------------------------------------------
# Punto de entrada
# -------------------------------------------------
if __name__ == "__main__":
    insertar_datos()
