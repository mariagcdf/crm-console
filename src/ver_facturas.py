import sqlite3

def ver_facturas():
    conn = sqlite3.connect("data/crm.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM facturas")
    filas = cursor.fetchall()

    for fila in filas:
        print(fila)

    conn.close()

if __name__ == "__main__":
    ver_facturas()
