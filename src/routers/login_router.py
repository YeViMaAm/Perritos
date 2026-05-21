# src/routers/login_router.py
import os
from fastapi import APIRouter, Request, Form, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from src.controllers.usuario_controller import autenticar_usuario, crear_usuario
from src.models.usuario import Usuario
from src.models.login import Login
from src.exceptions import (
    UsuarioVacio, UsuarioEspacios, 
    ContrasenaVacia, ContrasenaEspacios, 
    UsuarioNoExiste, ContrasenaIncorrecta
)

router = APIRouter(tags=["Autenticación"])

# CONFIGURACIÓN ABSOLUTA
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# 1. MOSTRAR EL LOGIN
@router.get("/")
def mostrar_login(request: Request, error: str = None, msg: str = None):
    # CAMBIO CRÍTICO PARA AZURE: usamos name= y context=
    return templates.TemplateResponse(
        name="index.html", 
        context={"request": request, "error": error, "msg": msg}
    )

# 2. PROCESAR EL LOGIN
@router.post("/login")
def procesar_login(usuario: str = Form(...), contrasena: str = Form(...)):
    try:
        datos_login = Login(usuario, contrasena) 
        usuario_valido = autenticar_usuario(datos_login.usuario, datos_login.contrasena)
        response = RedirectResponse(url="/lista", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(key="user_session", value=usuario_valido)
        return response
    except (UsuarioVacio, UsuarioEspacios, ContrasenaVacia, ContrasenaEspacios, 
            UsuarioNoExiste, ContrasenaIncorrecta) as e:
        return RedirectResponse(url=f"/?error={str(e)}", status_code=303)
    except Exception as e:
        return RedirectResponse(url="/?error=Error+inesperado", status_code=303)

# 3. PROCESAR REGISTRO
@router.post("/registro_usuario")
def registrar_nuevo_usuario(usuario: str = Form(...), contrasena: str = Form(...), nombre: str = Form(...)):
    nuevo = Usuario(username=usuario, password=contrasena, nombre_completo=nombre)
    if crear_usuario(nuevo):
        return RedirectResponse(url="/?msg=Usuario+creado+exitosamente", status_code=303)
    return RedirectResponse(url="/?error=El+usuario+ya+existe", status_code=303)

# 4. CERRAR SESIÓN
@router.get("/logout")
def logout():
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("user_session")
    return response