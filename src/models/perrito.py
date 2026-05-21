from typing import Optional
from sqlmodel import SQLModel, Field

class Perrito(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    tamano: str
    sexo: str
    edad: int
    raza: str
    ubicacion: str
    contacto: str
    vacunado: bool
    foto: Optional[str] = None
    registrado_por: Optional[str] = None