# src/routers/login_router.py
from fastapi import APIRouter, Request, Form, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

# Importamos controladores y modelos
from src.controllers.usuario_controller import autenticar_usuario, crear_usuario
from src.models.usuario import Usuario
from src.models.login import Login

# IMPORTANTE: Importamos tus excepciones personalizadas para poder atraparlas en el try/except
from src.exceptions import (
    UsuarioVacio, UsuarioEspacios, 
    ContrasenaVacia, ContrasenaEspacios, 
    UsuarioNoExiste, ContrasenaIncorrecta
)

router = APIRouter(tags=["Autenticación"])
templates = Jinja2Templates(directory="templates")

# 1. MOSTRAR EL LOGIN
@router.get("/")
def mostrar_login(request: Request, error: str = None, msg: str = None):
    """Muestra la página de inicio (Login)"""
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "error": error, 
        "msg": msg
    })

# 2. PROCESAR EL LOGIN
@router.post("/login")
def procesar_login(usuario: str = Form(...), contrasena: str = Form(...)):
    """Lógica para validar credenciales y crear cookie de sesión"""
    try:
        # Paso A: Validar formato (Lanza UsuarioVacio, UsuarioEspacios, etc.)
        datos_login = Login(usuario, contrasena) 
        
        # Paso B: Validar contra Base de Datos (Lanza UsuarioNoExiste o ContrasenaIncorrecta)
        usuario_valido = autenticar_usuario(datos_login.usuario, datos_login.contrasena)

        # Paso C: Si no hubo errores, crear redirección y cookie
        response = RedirectResponse(url="/lista", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(key="user_session", value=usuario_valido)
        return response

    except (UsuarioVacio, UsuarioEspacios, ContrasenaVacia, ContrasenaEspacios, 
            UsuarioNoExiste, ContrasenaIncorrecta) as e:
        # Capturamos tus excepciones y enviamos el mensaje al HTML a través de la URL
        return RedirectResponse(url=f"/?error={str(e)}", status_code=303)
    
    except Exception as e:
        # Captura cualquier otro error inesperado
        print(f"Error no controlado: {e}")
        return RedirectResponse(url="/?error=Error+inesperado+en+el+servidor", status_code=303)

# 3. PROCESAR REGISTRO DE NUEVO USUARIO
@router.post("/registro_usuario")
def registrar_nuevo_usuario(
    usuario: str = Form(...), 
    contrasena: str = Form(...), 
    nombre: str = Form(...)
):
    """Crea un nuevo usuario en la base de datos"""
    nuevo = Usuario(username=usuario, password=contrasena, nombre_completo=nombre)
    exito = crear_usuario(nuevo)
    
    if exito:
        return RedirectResponse(url="/?msg=Usuario+creado+exitosamente", status_code=303)
    else:
        return RedirectResponse(url="/?error=El+usuario+ya+existe", status_code=303)

# 4. CERRAR SESIÓN
@router.get("/logout")
def logout():
    """Elimina la cookie de sesión y redirige al login"""
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("user_session")
    return response