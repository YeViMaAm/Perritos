# src/routers/perrito_router.py
from fastapi import APIRouter, Request, Form, status, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from src.controllers.perrito_controller import (
    obtener_perritos, 
    crear_perrito, 
    eliminar_perrito,
    obtener_perrito_por_id
)
from src.models.perrito import Perrito

router = APIRouter(tags=["Perritos"])
templates = Jinja2Templates(directory="templates")

# 1. Ver la lista (Público: Todos pueden verla)
@router.get("/lista")
def mostrar_lista(request: Request):
    # Leemos la cookie para saber si hay alguien logueado
    usuario = request.cookies.get("user_session")
    
    # Traemos los perritos de la base de datos SQLModel
    lista_perritos = obtener_perritos()
    
    return templates.TemplateResponse("lista.html", {
        "request": request, 
        "perritos": lista_perritos,
        "usuario_logeado": usuario # Importante para ocultar/mostrar botones en el HTML
    })

# 2. Ver formulario de registro (Protegido)
@router.get("/registro")
def mostrar_registro(request: Request):
    usuario = request.cookies.get("user_session")
    if not usuario:
        # Si no está logueado, no puede ver el formulario
        return RedirectResponse(url="/?error=Debes+iniciar+sesion", status_code=303)
    
    return templates.TemplateResponse("registro.html", {"request": request})

# 3. Guardar perrito (Protegido y con etiqueta de dueño)
@router.post("/perritos")
def guardar_nuevo_perrito(
    request: Request,
    nombre: str = Form(...),
    raza: str = Form(...),
    edad: int = Form(...),
    tamano: str = Form(...),
    sexo: str = Form(...),
    ubicacion: str = Form(...),
    contacto: str = Form(...),
    vacunado: str = Form("No"),
    foto: str = Form(None)
):
    usuario = request.cookies.get("user_session")
    if not usuario:
        return RedirectResponse(url="/", status_code=303)

    # Creamos el objeto incluyendo quién lo registró (Punto 3 del docente)
    nuevo = Perrito(
        nombre=nombre, raza=raza, edad=edad, tamano=tamano,
        sexo=sexo, ubicacion=ubicacion, contacto=contacto,
        foto=foto, vacunado=(vacunado == "Sí"),
        registrado_por=usuario # <--- Aquí queda guardado el dueño
    )
    
    crear_perrito(nuevo)
    return RedirectResponse(url="/lista", status_code=303)

# 4. Borrar perrito (Protegido: Solo el dueño)
@router.get("/borrar/{id}")
def borrar_perrito_ruta(request: Request, id: int):
    usuario = request.cookies.get("user_session")
    if not usuario:
        return RedirectResponse(url="/", status_code=303)
    
    # El controlador se encarga de verificar si 'usuario' es el dueño
    exito = eliminar_perrito(id, usuario)
    
    if exito:
        return RedirectResponse(url="/lista", status_code=303)
    else:
        # Si no es el dueño, lanzamos un error 401 (No autorizado) - Punto 4 del docente
        raise HTTPException(status_code=401, detail="No tienes permiso para borrar este registro")