from fastapi import FastAPI

# creamos la instancia de FastAPY 
app = FastAPI()

#Definir al menos un endpoint
@app.get("/")
def home():
    return {"mensaje": "Mi API esta funcionando"}

