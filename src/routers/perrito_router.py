# src/routers/perrito_router.py
from fastapi import APIRouter, Request, Form, status, HTTPException, File, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import shutil
import os

# Importamos controladores y modelos
from src.controllers.perrito_controller import (
    obtener_perritos, 
    crear_perrito, 
    eliminar_perrito,
    obtener_perrito_por_id
)
from src.models.perrito import Perrito

router = APIRouter(tags=["Perritos"])
templates = Jinja2Templates(directory="templates")

# 1. VER LA LISTA (Público: Todos pueden verla)
@router.get("/lista")
def mostrar_lista(request: Request):
    """Muestra todos los perritos registrados"""
    usuario = request.cookies.get("user_session")
    lista_perritos = obtener_perritos()
    
    return templates.TemplateResponse("lista.html", {
        "request": request, 
        "perritos": lista_perritos,
        "usuario_logeado": usuario
    })

# 2. VER FORMULARIO DE REGISTRO (Protegido)
@router.get("/registro")
def mostrar_registro(request: Request):
    """Muestra el formulario para registrar un perrito (solo si hay sesión)"""
    usuario = request.cookies.get("user_session")
    if not usuario:
        return RedirectResponse(url="/?error=Debes+iniciar+sesion", status_code=303)
    
    return templates.TemplateResponse("registro.html", {"request": request})

# 3. GUARDAR PERRITO (Protegido y con subida de archivo)
@router.post("/perritos")
async def guardar_nuevo_perrito(
    request: Request,
    nombre: str = Form(...),
    raza: str = Form(...),
    edad: int = Form(...),
    tamano: str = Form(...),
    sexo: str = Form(...),
    ubicacion: str = Form(...),
    contacto: str = Form(...),
    vacunado: str = Form("No"),
    foto: UploadFile = File(...) # <--- Recibe el archivo binario
):
    """Procesa el formulario y guarda la imagen en el servidor"""
    usuario = request.cookies.get("user_session")
    if not usuario:
        return RedirectResponse(url="/", status_code=303)

    # --- Lógica de Almacenamiento de Archivo ---
    
    # Creamos un nombre de archivo único para evitar que se sobrescriban
    # Ejemplo: "juan_fido.jpg"
    nombre_archivo = f"{usuario}_{foto.filename}"
    ruta_destino = os.path.join("static", "uploads", nombre_archivo)
    
    # Guardamos el archivo físicamente en la carpeta static/uploads
    try:
        with open(ruta_destino, "wb") as buffer:
            shutil.copyfileobj(foto.file, buffer)
    except Exception as e:
        print(f"Error al guardar la imagen: {e}")
        # Si falla el guardado, podemos poner una imagen por defecto o lanzar error
        nombre_archivo = "default.jpg"

    # --- Lógica de Base de Datos ---

    # Creamos el objeto Perrito con el NOMBRE del archivo en el campo foto
    nuevo = Perrito(
        nombre=nombre, 
        raza=raza, 
        edad=edad, 
        tamano=tamano,
        sexo=sexo, 
        ubicacion=ubicacion, 
        contacto=contacto,
        foto=nombre_archivo, # <--- Se guarda el nombre del archivo guardado
        vacunado=(vacunado == "Sí"),
        registrado_por=usuario
    )
    
    crear_perrito(nuevo)
    return RedirectResponse(url="/lista", status_code=303)

# 4. BORRAR PERRITO (Protegido: Solo el dueño)
@router.get("/borrar/{id}")
def borrar_perrito_ruta(request: Request, id: int):
    """Elimina un registro si el usuario es el dueño"""
    usuario = request.cookies.get("user_session")
    if not usuario:
        return RedirectResponse(url="/", status_code=303)
    
    # El controlador verifica la propiedad del registro
    exito = eliminar_perrito(id, usuario)
    
    if exito:
        return RedirectResponse(url="/lista", status_code=303)
    else:
        raise HTTPException(status_code=401, detail="No tienes permiso para borrar este registro")

@router.get("/perrito/{id}")
def ver_detalle_perrito(request: Request, id: int):
    """Muestra la información completa de un perrito específico"""
    usuario = request.cookies.get("user_session")
    
    # Buscamos el perrito por ID usando el controlador que ya tienes
    perrito = obtener_perrito_por_id(id)
    
    if not perrito:
        raise HTTPException(status_code=404, detail="El perrito no existe")
    
    return templates.TemplateResponse("detalle.html", {
        "request": request,
        "perrito": perrito,
        "usuario_logeado": usuario
    })

@router.get("/editar/{id}")
def mostrar_formulario_edicion(request: Request, id: int):
    usuario = request.cookies.get("user_session")
    perrito = obtener_perrito_por_id(id)

    if not usuario:
        return RedirectResponse(url="/?error=Inicia+sesion+para+editar", status_code=303)
    
    if not perrito or perrito.registrado_por != usuario:
        raise HTTPException(status_code=401, detail="No tienes permiso para editar este perrito")

    return templates.TemplateResponse("editar.html", {
        "request": request,
        "perrito": perrito,
        "usuario_logeado": usuario
    })

# B. PROCESAR LA EDICIÓN
@router.post("/editar/{id}")
async def procesar_edicion(
    request: Request,
    id: int,
    nombre: str = Form(...),
    raza: str = Form(...),
    edad: int = Form(...),
    tamano: str = Form(...),
    sexo: str = Form(...),
    ubicacion: str = Form(...),
    contacto: str = Form(...),
    vacunado: str = Form("No"),
    foto: UploadFile = File(None) # Opcional en edición
):
    usuario = request.cookies.get("user_session")
    if not usuario: return RedirectResponse(url="/", status_code=303)

    # Si subió una foto nueva, la guardamos. Si no, mantenemos la anterior.
    perrito_actual = obtener_perrito_por_id(id)
    nombre_foto = perrito_actual.foto

    if foto and foto.filename:
        nombre_foto = f"{usuario}_{foto.filename}"
        ruta = os.path.join("static", "uploads", nombre_foto)
        with open(ruta, "wb") as buffer:
            shutil.copyfileobj(foto.file, buffer)

    # Creamos un objeto con los nuevos datos
    datos_nuevos = Perrito(
        nombre=nombre, raza=raza, edad=edad, tamano=tamano,
        sexo=sexo, ubicacion=ubicacion, contacto=contacto,
        foto=nombre_foto, vacunado=(vacunado == "Sí")
    )

    actualizar_perrito(id, datos_nuevos, usuario)
    return RedirectResponse(url="/lista", status_code=303)