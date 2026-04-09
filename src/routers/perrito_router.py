from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from src.controllers.perrito_controller import (
    obtener_perritos,
    crear_perrito,
    obtener_perrito_por_id
)
from src.models.perrito import Perrito

router = APIRouter()

templates = Jinja2Templates(directory="templates")

# Mostrar formulario de registro
@router.get("/registro")
def mostrar_registro(request: Request):
    return templates.TemplateResponse("registro.html", {"request": request})

# Mostrar lista de perritos
@router.get("/lista")
def mostrar_lista(request: Request):
    perritos = obtener_perritos()
    return templates.TemplateResponse("lista.html", {
        "request": request,
        "perritos": perritos
    })

# Crear perrito (desde formulario)
@router.post("/perritos")
def guardar_perrito(
    id: int = Form(...),
    nombre: str = Form(...),
    tamano: str = Form(...),
    sexo: str = Form(...),
    edad: int = Form(...),
    raza: str = Form(...),
    ubicacion: str = Form(...),
    contacto: str = Form(...),
    vacunado: bool = Form(False)
):
    data = Perrito(
        id=id,
        nombre=nombre,
        tamano=tamano,
        sexo=sexo,
        edad=edad,
        raza=raza,
        ubicacion=ubicacion,
        contacto=contacto,
        vacunado=vacunado
    )

    crear_perrito(data)

    return RedirectResponse(url="/lista", status_code=303)

# Obtener perrito por id (API)
@router.get("/perritos/{id}")
def obtener_perrito(id: int):
    perrito = obtener_perrito_por_id(id)
    return perrito