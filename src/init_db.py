from db import conectar

def crear_tablas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            apellidos TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            telefono TEXT,
            direccion TEXT,
            fecha_registro TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    print("Base de datos inicializada.")

if __name__ == "__main__":
    crear_tablas()
