# src/controllers/usuario_controller.py
from sqlmodel import select
from src.database import db_singleton
from src.models.usuario import Usuario

def crear_usuario(nuevo_usuario: Usuario):
    with db_singleton.get_session() as session:
        try:
            session.add(nuevo_usuario)
            session.commit()
            return True
        except: # Si el usuario ya existe (unique constraint)
            return False

def autenticar_usuario(username_ingresado, password_ingresada):
    with db_singleton.get_session() as session:
        statement = select(Usuario).where(Usuario.username == username_ingresado)
        usuario_db = session.exec(statement).first()

        if usuario_db and usuario_db.password == password_ingresada:
            return {"success": True, "usuario": usuario_db.username}
        return {"success": False, "error": "Credenciales inválidas"}