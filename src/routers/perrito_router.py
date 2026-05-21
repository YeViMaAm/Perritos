# src/routers/perrito_router.py
import os
import shutil
from fastapi import APIRouter, Request, Form, status, HTTPException, File, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from src.controllers.perrito_controller import (
    obtener_perritos, crear_perrito, eliminar_perrito,
    obtener_perrito_por_id, actualizar_perrito
)
from src.models.perrito import Perrito

router = APIRouter(tags=["Perritos"])

# CONFIGURACIÓN ROBUSTA DE TEMPLATES (Ruta absoluta)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# 1. VER LA LISTA
@router.get("/lista")
def mostrar_lista(request: Request):
    usuario = request.cookies.get("user_session")
    lista_perritos = obtener_perritos()
    return templates.TemplateResponse("lista.html", {
        "request": request, 
        "perritos": lista_perritos,
        "usuario_logeado": usuario
    })

# 2. VER REGISTRO
@router.get("/registro")
def mostrar_registro(request: Request):
    usuario = request.cookies.get("user_session")
    if not usuario:
        return RedirectResponse(url="/?error=Debes+iniciar+sesion", status_code=303)
    return templates.TemplateResponse("registro.html", {"request": request})

# 3. GUARDAR PERRITO
@router.post("/perritos")
async def guardar_nuevo_perrito(
    request: Request, nombre: str = Form(...), raza: str = Form(...),
    edad: int = Form(...), tamano: str = Form(...), sexo: str = Form(...),
    ubicacion: str = Form(...), contacto: str = Form(...),
    vacunado: str = Form("No"), foto: UploadFile = File(...)
):
    usuario = request.cookies.get("user_session")
    if not usuario: return RedirectResponse(url="/", status_code=303)

    nombre_archivo = f"{usuario}_{foto.filename}"
    ruta_destino = os.path.join(BASE_DIR, "static", "uploads", nombre_archivo)
    
    try:
        with open(ruta_destino, "wb") as buffer:
            shutil.copyfileobj(foto.file, buffer)
    except:
        nombre_archivo = "default.jpg"

    nuevo = Perrito(
        nombre=nombre, raza=raza, edad=edad, tamano=tamano,
        sexo=sexo, ubicacion=ubicacion, contacto=contacto,
        foto=nombre_archivo, vacunado=(vacunado == "Sí"),
        registrado_por=usuario
    )
    crear_perrito(nuevo)
    return RedirectResponse(url="/lista", status_code=303)

# 4. DETALLE, EDITAR Y BORRAR
@router.get("/perrito/{id}")
def ver_detalle_perrito(request: Request, id: int):
    perrito = obtener_perrito_por_id(id)
    if not perrito: raise HTTPException(status_code=404)
    return templates.TemplateResponse("detalle.html", {
        "request": request, "perrito": perrito, "usuario_logeado": request.cookies.get("user_session")
    })

@router.get("/editar/{id}")
def mostrar_formulario_edicion(request: Request, id: int):
    usuario = request.cookies.get("user_session")
    perrito = obtener_perrito_por_id(id)
    if not usuario or not perrito or perrito.registrado_por != usuario:
        return RedirectResponse(url="/lista", status_code=303)
    return templates.TemplateResponse("editar.html", {"request": request, "perrito": perrito, "usuario_logeado": usuario})

@router.post("/editar/{id}")
async def procesar_edicion(
    request: Request, id: int, nombre: str = Form(...), raza: str = Form(...),
    edad: int = Form(...), tamano: str = Form(...), sexo: str = Form(...),
    ubicacion: str = Form(...), contacto: str = Form(...),
    vacunado: str = Form("No"), foto: UploadFile = File(None)
):
    usuario = request.cookies.get("user_session")
    perrito_actual = obtener_perrito_por_id(id)
    nombre_foto = perrito_actual.foto

    if foto and foto.filename:
        nombre_foto = f"{usuario}_{foto.filename}"
        ruta = os.path.join(BASE_DIR, "static", "uploads", nombre_foto)
        with open(ruta, "wb") as buffer:
            shutil.copyfileobj(foto.file, buffer)

    datos_nuevos = Perrito(
        nombre=nombre, raza=raza, edad=edad, tamano=tamano,
        sexo=sexo, ubicacion=ubicacion, contacto=contacto,
        foto=nombre_foto, vacunado=(vacunado == "Sí")
    )
    actualizar_perrito(id, datos_nuevos, usuario)
    return RedirectResponse(url="/lista", status_code=303)

@router.get("/borrar/{id}")
def borrar_perrito_ruta(request: Request, id: int):
    usuario = request.cookies.get("user_session")
    if eliminar_perrito(id, usuario):
        return RedirectResponse(url="/lista", status_code=303)
    raise HTTPException(status_code=401)