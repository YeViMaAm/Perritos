import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src.routers import login_router, perrito_router

app = FastAPI(title="Adopción de Perritos Candy")

# --- CONFIGURACIÓN DE ARCHIVOS ESTÁTICOS ---

# 1. Definimos las rutas de las carpetas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(os.path.dirname(BASE_DIR), "static")
UPLOADS_DIR = os.path.join(STATIC_DIR, "uploads")

# 2. Creamos las carpetas si no existen (Esto cumple con el requisito de automatización)
if not os.path.exists(UPLOADS_DIR):
    os.makedirs(UPLOADS_DIR, exist_ok=True)
    print(f"✅ Carpeta creada en: {UPLOADS_DIR}")

# 3. Montamos la carpeta 'static' para que sea accesible desde el navegador
# Ejemplo: si subes 'fido.jpg', se verá en http://localhost:8000/static/uploads/fido.jpg
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# --- INCLUSIÓN DE RUTAS ---

# El login_router maneja la raíz "/" y la autenticación
app.include_router(login_router.router)

# El perrito_router maneja "/lista", "/registro" y la gestión de perritos
app.include_router(perrito_router.router)