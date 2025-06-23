from db import conectar

def crear_tablas():
    conn = conectar()
    cursor = conn.cursor()

    # Tabla de usuarios
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

    # Tabla de facturas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS facturas (
            id TEXT PRIMARY KEY,
            usuario_id TEXT NOT NULL,
            concepto TEXT NOT NULL,
            cantidad REAL NOT NULL,
            fecha TEXT NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    ''')

    conn.commit()
    conn.close()
    print("Base de datos inicializada.")

if __name__ == "__main__":
    crear_tablas()
