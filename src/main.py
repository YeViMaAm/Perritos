# src/main.py
from fastapi import FastAPI
from src.routers import login_router, perrito_router

app = FastAPI(title="Adopción de Perritos Candy")

# No necesitamos el @app.get("/") aquí porque el login_router ya lo maneja
# Al incluir los routers, FastAPI busca las rutas en orden.

app.include_router(login_router.router)
app.include_router(perrito_router.router)
