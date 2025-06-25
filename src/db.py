import sqlite3
import os

def conectar():
    ruta_db = os.path.join(os.path.dirname(__file__), '..', 'data', 'crm.db')
    return sqlite3.connect(ruta_db)

def crear_tablas():
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id TEXT PRIMARY KEY,
        nombre TEXT NOT NULL,
        apellidos TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        telefono TEXT,
        direccion TEXT,
        fecha_registro TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS facturas (
        numero TEXT PRIMARY KEY,
        usuario_id TEXT NOT NULL,
        fecha_emision TEXT NOT NULL,
        descripcion TEXT NOT NULL,
        monto REAL NOT NULL,
        estado TEXT NOT NULL CHECK(estado IN ('Pendiente','Pagada','Cancelada')),
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
    )
    ''')

    conn.commit()
    conn.close()
    
if __name__ == "__main__":
    crear_tablas()