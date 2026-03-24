from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request, FastAPI, HTTPException, Form
from pydantic import BaseModel

app = FastAPI()
templates = Jinja2Templates(directory="templates")
perritos = []

@app.get("/")
def home():
    return {"mensaje": "Mi API esta funcionando, nuevo mensaje"}

@app.get("/inicio")
def mostrar_inicio(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/registro")
def mostrar_registro(request: Request):
    return templates.TemplateResponse("registro.html", {"request": request})


@app.get("/lista")
def mostrar_lista(request: Request):
    return templates.TemplateResponse("lista.html", {
        "request": request,
        "perritos": perritos
    })

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



@app.get("/perritos")
def obtener_perritos(sexo: str = None):
    if sexo:
        return [p for p in perritos if p["sexo"].lower() == sexo.lower()]
    return perritos


@app.post("/perritos")
def crear_perrito(
    id: int = Form(...),
    nombre: str = Form(...),
    tamano: str = Form(...),
    sexo: str = Form(...),
    edad: int = Form(...),
    raza: str = Form(...),
    ubicacion: str = Form(...),
    contacto: str = Form(...),
    vacunado: bool = Form(False)
):
    perrito = {
        "id": id,
        "nombre": nombre,
        "tamano": tamano,
        "sexo": sexo,
        "edad": edad,
        "raza": raza,
        "ubicacion": ubicacion,
        "contacto": contacto,
        "vacunado": vacunado
    }

    perritos.append(perrito)

    return RedirectResponse(url="/lista", status_code=303)


@app.get("/perritos/{id}")
def obtener_perrito(id: int):
    for p in perritos:
        if p["id"] == id:
            return p
    raise HTTPException(status_code=404, detail="Perrito no encontrado")