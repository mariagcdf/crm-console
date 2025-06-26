
readme = """
# CRM Console App

Este es un proyecto de consola desarrollado en Python que simula un sistema básico de gestión de relaciones con clientes (CRM). Permite registrar usuarios, generar facturas, consultar información y realizar análisis financieros. Está diseñado para usarse en local y utiliza SQLite como base de datos.

---

## 📁 Estructura del proyecto

crm-console/
│
├── data/
│   └── crm.db              # Base de datos SQLite
│
├── src/
│   ├── main.py             # Punto de entrada de la aplicación
│   ├── ui.py               # Interfaz de usuario en consola
│   ├── core.py             # Lógica principal del programa
│   ├── db.py               # Funciones de conexión a la base de datos
│   ├── crear_db.py         # Script para poblar la base de datos con datos aleatorios (Faker)
│
├── README.md               # Este archivo
└── requirements.txt        # Librerías necesarias

---

## 🔧 Requisitos

- Python 3.10+
- Biblioteca externa `Faker` para generación de datos (solo para el script `crear_db.py`), que crea una base de datos de ejmplo para poder probar el programa.

Instalación del entorno virtual y dependencias:

python -m venv venv
venv\\Scripts\\activate       # En Windows
pip install -r requirements.txt

---

## ▶️ Ejecución del programa

Desde la carpeta src, ejecutar el archivo principal:

python main.py

---

## 🧠 Funcionalidades principales

1. Registrar usuario  
   Introduce nombre, apellidos, email, teléfono (opcional), dirección (opcional). Se genera un ID automático.

2. Buscar usuario por email  
   Permite buscar un usuario por su dirección de correo electrónico.

3. Crear factura  
   Registra una factura asociada a un usuario ya existente, introduciendo descripción y cantidad.

4. Mostrar todos los usuarios  
   Lista los usuarios registrados.

5. Mostrar facturas de un usuario  
   Solicita el email y muestra todas las facturas asociadas a ese usuario.

6. Resumen financiero  
   Muestra el total facturado por cada usuario y su número de facturas.

7. Modificar usuario  
   Permite actualizar cualquier campo, incluyendo email, utilizando como referencia el nombre y apellidos.  
   Nota: si hay varios usuarios con el mismo nombre y apellidos, se advierte de la ambigüedad y se solicita una identificación adicional.

8. Eliminar usuario  
   Borra completamente a un usuario y sus facturas. Se utiliza el nombre y apellidos como identificador.  
   Si hay más de un usuario con ese nombre/apellido, se muestran y se solicita elegir uno por ID.

---

## 🧪 Script de creación de datos aleatorios

Paso 1: Crear la base de datos y su estructura
python src/db.py

Paso 2: Rellenar la base de datos con datos de prueba
python src/crear_db.py


---

## Diagrama de flujo general del CRM:

![alt text](<Editor _ Mermaid Chart-2025-06-26-111132.png>)

