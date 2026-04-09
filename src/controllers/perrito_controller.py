perritos = []

def obtener_perritos(sexo=None):
    if sexo:
        return [p for p in perritos if p["sexo"].lower() == sexo.lower()]
    return perritos


def crear_perrito(data):
    perrito = {
        "id": data.id,
        "nombre": data.nombre,
        "tamano": data.tamano,
        "sexo": data.sexo,
        "edad": data.edad,
        "raza": data.raza,
        "ubicacion": data.ubicacion,
        "contacto": data.contacto,
        "vacunado": data.vacunado
    }

    perritos.append(perrito)
    return perrito


def obtener_perrito_por_id(id):
    for p in perritos:
        if p["id"] == id:
            return p
    return None