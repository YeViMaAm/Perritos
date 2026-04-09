
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.routers import login_router, perrito_router

# Crear la aplicación
app = FastAPI()

# ✅ Configurar archivos estáticos (CSS)
app.mount("/static", StaticFiles(directory="src/static"), name="static")

# ✅ Conectar routers
app.include_router(login_router.router)
app.include_router(perrito_router.router)
