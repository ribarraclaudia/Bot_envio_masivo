from fastapi import FastAPI
from pydantic import BaseModel
import json
import os

app = FastAPI()

# Definir la estructura del mensaje
class Mensaje(BaseModel):
    numero: str
    mensaje: str

# Ruta para recibir los mensajes y guardarlos en un JSON
@app.post("/enviar_mensaje/")
async def enviar_mensaje(mensajes: dict[str, str]):
    archivo_json = "mensajes.json"

    # Verificar si el archivo existe
    if os.path.exists(archivo_json):
        # Cargar datos existentes
        with open(archivo_json, "r") as file:
            data = json.load(file)
    else:
        # Crear nuevo archivo
        data = {}

    # Agregar los nuevos mensajes al JSON
    data.update(mensajes)

    # Guardar los datos actualizados
    with open(archivo_json, "w") as file:
        json.dump(data, file, indent=4)

    return {"status": "Mensajes guardados en JSON", "data": mensajes}
