from sqlmodel import select
from src.database import db_singleton
from src.models.usuario import Usuario

from src.exceptions import UsuarioNoExiste, ContrasenaIncorrecta

def crear_usuario(nuevo_usuario: Usuario):
    with db_singleton.get_session() as session:
        try:
            session.add(nuevo_usuario)
            session.commit()
            return True
        except:
            return False

def autenticar_usuario(username_ingresado, password_ingresada):
    with db_singleton.get_session() as session:
        statement = select(Usuario).where(Usuario.username == username_ingresado)
        usuario_db = session.exec(statement).first()

        # 1. Si no existe el usuario en la DB
        if not usuario_db:
            raise UsuarioNoExiste(f"El usuario '{username_ingresado}' no existe.")

        # 2. Si la contraseña no coincide
        if usuario_db.password != password_ingresada:
            raise ContrasenaIncorrecta("La contraseña ingresada es incorrecta.")

        # 3. Si todo está bien, retornamos el nombre de usuario para la sesión
        return usuario_db.username