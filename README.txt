API de Compostaje - Instrucciones de ejecucion
=============================================

Este proyecto es una API desarrollada con FastAPI y SQLAlchemy para gestionar usuarios, diario, ventas, retos, logros y recordatorios.

Requisitos
----------
- Python 3.10 o superior
- pip
- Git (opcional, si se clona el proyecto)

1. Entrar a la carpeta del proyecto
-----------------------------------
cd c:\Users\Pedro\.vscode\Base_datos_lombriaventura

2. Crear y activar un entorno virtual
------------------------------------
Windows (PowerShell):
py -m venv venv
.\venv\Scripts\Activate.ps1

Windows (Git Bash / Bash):
python -m venv venv
source venv/Scripts/activate

Linux / macOS:
python3 -m venv venv
source venv/bin/activate

3. Instalar dependencias
-----------------------
pip install -r requirements.txt

4. Configuracion de base de datos
---------------------------------
La aplicacion intenta conectar a PostgreSQL usando estas variables de entorno:
- DB_USER
- DB_PASSWORD
- DB_HOST
- DB_PORT
- DB_NAME
- DATABASE_URL (si se define, tiene prioridad)

Si PostgreSQL no esta disponible, la API automaticamente usara SQLite y creara el archivo:
- compostaje.db

5. Ejecutar la API
------------------
uvicorn main:app --reload --host 0.0.0.0 --port 8000

Una vez iniciada, la API quedara disponible en:
- http://127.0.0.1:8000/
- http://127.0.0.1:8000/docs  (documentacion interactiva de Swagger)
- http://127.0.0.1:8000/redoc

6. Probar la API
----------------
Puedes probar la ruta principal con:
http://127.0.0.1:8000/

O usar Swagger en:
http://127.0.0.1:8000/docs

Ejemplo de creacion de usuario:
POST /usuarios
{
  "nombre": "Ana",
  "email": "ana@example.com",
  "nombre_usuario": "ana123"
}

Notas importantes
----------------
- Al iniciar la aplicacion, las tablas se crean automaticamente si no existen.
- El archivo compostaje.db se generara automaticamente si no se usa PostgreSQL.
- Si cambias la configuracion de la base de datos, reinicia el servidor.
