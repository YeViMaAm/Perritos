from typing import Optional
from sqlmodel import SQLModel, Field

class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True) # unique=True garantiza que no se repitan usuarios
    password: str 
    nombre_completo: str