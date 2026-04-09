from src.models.login import Login

def autenticar_usuario(usuario, contrasena):
    try:
        user = login(usuario, contrasena)
        return {"success": True, "usuario": user.usuario}
    except Exception as e:
        return {"success": False, "error": str(e)}