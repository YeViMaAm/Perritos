from sqlmodel import select, col  # Añadimos 'col' para búsquedas inteligentes
from src.database import db_singleton
from src.models.perrito import Perrito

def obtener_perritos():
    """Obtiene todos los perritos de la base de datos"""
    with db_singleton.get_session() as session:
        statement = select(Perrito)
        return session.exec(statement).all()

# --- NUEVA FUNCIÓN DE BÚSQUEDA ---
def buscar_perritos(criterio: str, valor: str):
    """Filtra perritos por nombre, raza, ubicación o tamaño"""
    with db_singleton.get_session() as session:
        statement = select(Perrito)
        
        if criterio == "nombre":
            statement = statement.where(col(Perrito.nombre).contains(valor))
        elif criterio == "raza":
            statement = statement.where(col(Perrito.raza).contains(valor))
        elif criterio == "ubicacion":
            statement = statement.where(col(Perrito.ubicacion).contains(valor))
        elif criterio == "tamano":
            # Para tamaño usamos coincidencia exacta
            statement = statement.where(Perrito.tamano == valor)
            
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
        perrito_db = session.get(Perrito, id)
        
        if not perrito_db:
            return None 
        
        if perrito_db.registrado_por != usuario_actual:
            return "No autorizado"

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
        
        if perrito_db and perrito_db.registrado_por == usuario_actual:
            session.delete(perrito_db)
            session.commit()
            return True
            
        return False