# src/controllers/perrito_controller.py
from sqlmodel import select
from src.database import db_singleton
from src.models.perrito import Perrito

def obtener_perritos():
    """Obtiene todos los perritos de la base de datos"""
    with db_singleton.get_session() as session:
        statement = select(Perrito)
        return session.exec(statement).all()

def crear_perrito(data: Perrito):
    """Guarda un nuevo perrito en la base de datos"""
    with db_singleton.get_session() as session:
        session.add(data)
        session.commit()
        session.refresh(data)
        return data

def obtener_perrito_por_id(id: int):
    """Busca un perrito por su ID"""
    with db_singleton.get_session() as session:
        return session.get(Perrito, id)

def actualizar_perrito(id: int, data_nueva: Perrito, usuario_actual: str):
    """Actualiza un perrito solo si el usuario es el dueño"""
    with db_singleton.get_session() as session:
        # 1. Buscamos el perrito actual en la DB
        perrito_db = session.get(Perrito, id)
        
        if not perrito_db:
            return None # No existe
        
        # 2. VALIDACIÓN DE DUEÑO: ¿El que intenta editar es el mismo que lo registró?
        if perrito_db.registrado_por != usuario_actual:
            return "No autorizado"

        # 3. Actualizamos los campos con la nueva información
        # Convertimos los datos nuevos a diccionario
        datos_actualizados = data_nueva.model_dump(exclude_unset=True)
        for llave, valor in datos_actualizados.items():
            setattr(perrito_db, llave, valor)
        
        session.add(perrito_db)
        session.commit()
        session.refresh(perrito_db)
        return perrito_db

def eliminar_perrito(id: int, usuario_actual: str):
    """Elimina un perrito solo si el usuario es el dueño"""
    with db_singleton.get_session() as session:
        perrito_db = session.get(Perrito, id)
        
        # Solo eliminamos si existe y si el usuario es el dueño
        if perrito_db and perrito_db.registrado_por == usuario_actual:
            session.delete(perrito_db)
            session.commit()
            return True
            
        return False