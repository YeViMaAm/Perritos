# src/routers/login_router.py
from fastapi import APIRouter, Request, Form, status, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from src.controllers.usuario_controller import autenticar_usuario, crear_usuario
from src.models.usuario import Usuario

router = APIRouter(tags=["Autenticación"])
templates = Jinja2Templates(directory="templates")

# 1. Mostrar el Login
@router.get("/")
def mostrar_login(request: Request, error: str = None, msg: str = None):
    # Pasamos 'error' o 'msg' para mostrarlos en el HTML si existen
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "error": error, 
        "msg": msg
    })

# 2. Procesar el Login
@router.post("/login")
def procesar_login(usuario: str = Form(...), contrasena: str = Form(...)):
    # Buscamos en la base de datos de usuarios
    resultado = autenticar_usuario(usuario, contrasena)

    if resultado["success"]:
        # Creamos la redirección a la lista
        response = RedirectResponse(url="/lista", status_code=status.HTTP_303_SEE_OTHER)
        # Creamos la Cookie de sesión
        response.set_cookie(key="user_session", value=resultado["usuario"])
        return response
    else:
        # Si falla, regresamos al login con el error en la URL
        return RedirectResponse(url=f"/?error={resultado['error']}", status_code=303)

# 3. Procesar Registro de Nuevo Usuario
@router.post("/registro_usuario")
def registrar_nuevo_usuario(
    usuario: str = Form(...), 
    contrasena: str = Form(...), 
    nombre: str = Form(...)
):
    nuevo = Usuario(username=usuario, password=contrasena, nombre_completo=nombre)
    exito = crear_usuario(nuevo)
    
    if exito:
        return RedirectResponse(url="/?msg=Usuario+creado+exitosamente", status_code=303)
    else:
        return RedirectResponse(url="/?error=El+usuario+ya+existe", status_code=303)

# 4. Cerrar Sesión
@router.get("/logout")
def logout():
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    # Al borrar la cookie, el usuario vuelve a ser "invitado"
    response.delete_cookie("user_session")
    return response