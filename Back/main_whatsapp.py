from fastapi import FastAPI
from pydantic import BaseModel
import requests
import json
import os

app = FastAPI()

# Definir la estructura del mensaje
class Mensaje(BaseModel):
    numero: str
    mensaje: str

ACCESS_TOKEN = 'TU_ACCESS_TOKEN_DE_WHATSAPP'
WHATSAPP_API_URL = 'https://graph.facebook.com/v16.0/tu_numero_de_telefono/messages'

# Ruta para recibir los mensajes, enviarlos por WhatsApp y guardarlos en un JSON
@app.post("/enviar_mensaje/")
async def enviar_mensaje(mensajes: Mensaje):
    # Enviar mensaje a través de la API de WhatsApp
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": mensajes.numero,
        "type": "text",
        "text": {
            "body": mensajes.mensaje
        }
    }

    response = requests.post(WHATSAPP_API_URL, json=payload, headers=headers)
    
    # Imprimir respuesta para ver si fue exitosa
    print("Respuesta de WhatsApp API:", response.json())
    
    # Guardar el mensaje en un archivo JSON para registrar lo enviado
    archivo_json = "mensajes.json"

    # Verificar si el archivo existe
    if os.path.exists(archivo_json):
        # Cargar datos existentes
        with open(archivo_json, "r") as file:
            data = json.load(file)
    else:
        # Crear nuevo archivo
        data = {}

    # Agregar el nuevo mensaje al JSON
    data[mensajes.numero] = mensajes.mensaje

    # Guardar los datos actualizados
    with open(archivo_json, "w") as file:
        json.dump(data, file, indent=4)

    return {
        "status": "Mensaje enviado a WhatsApp y guardado en JSON",
        "whatsapp_response": response.json()
    }
