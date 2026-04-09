from pydantic import BaseModel

class Perrito(BaseModel):
    id: int
    nombre: str
    tamano: str
    sexo: str
    edad: int
    raza: str
    ubicacion: str
    contacto: str
    vacunado: bool