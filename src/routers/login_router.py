from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from src.controllers.login_controller import autenticar_usuario

router = APIRouter()

templates = Jinja2Templates(directory="src/templates")

# Mostrar página principal (login)
@router.get("/")
def mostrar_login(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Procesar login
@router.post("/login")
def procesar_login(request: Request, usuario: str = Form(...), contrasena: str = Form(...)):
    resultado = autenticar_usuario(usuario, contrasena)

    if resultado["success"]:
        # Lista de perritos de prueba
        perritos = [
            {"nombre": "Max", "raza": "Labrador", "edad": 2, "vacunado": True},
            {"nombre": "Luna", "raza": "Criollo", "edad": 1, "vacunado": False}
        ]

        return templates.TemplateResponse("lista.html", {
            "request": request,
            "perritos": perritos
        })
    else:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": resultado["error"]
        })