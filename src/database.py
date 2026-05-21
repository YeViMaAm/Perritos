from sqlmodel import SQLModel, create_engine, Session

class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            sqlite_url = "sqlite:///perritos.db"
            cls._instance.engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})
            
            # se importan ambos para que SQLModel cree las dos tablas
            from src.models.perrito import Perrito
            from src.models.usuario import Usuario
            SQLModel.metadata.create_all(cls._instance.engine)
            
        return cls._instance

    def get_session(self):
        return Session(self.engine)

db_singleton = DatabaseConnection()