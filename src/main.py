
from fastapi import FastAPI
from src.routers import login_router, perrito_router

app = FastAPI()

# Conectar routers
app.include_router(login_router.router)
app.include_router(perrito_router.router)
