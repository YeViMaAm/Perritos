from src.models.login import Login

def autenticar_usuario(usuario, contrasena):
    try:
        login = Login(usuario, contrasena)  # 
        return {"success": True, "usuario": usuario}
    except Exception as e:
        return {"success": False, "error": str(e)}
