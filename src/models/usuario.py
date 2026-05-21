from typing import Optional
from sqlmodel import SQLModel, Field

class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # unique=True garantiza que no se repitan usuarios
    username: str = Field(unique=True, index=True) 
    password: str 
    nombre_completo: str