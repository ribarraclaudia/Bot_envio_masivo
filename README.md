# Mi Proyecto de Mensajería

Este proyecto consta de una aplicación web con dos componentes principales: una interfaz de usuario con Streamlit y un servicio de backend con FastAPI.

## Estructura del Proyecto

```plaintext
bot_whatsapp
├── Back
│   ├── main.py
│   └── mensajes.json
├── Front
│   ├── pages
│   │   ├── resources
│   │   │   ├── contacts.xlsx
│   │   │   ├── contador_mensajes.csv
│   │   │   └── mensajes_predefinidos.xlsx
│   │   ├── 1_📞_contact_manager.py
│   │   └── 2_✉️_message_manager.py
│   ├── homepage.py
├── .gitignore
├── README.md
└── requirements.txt
```

## Requisitos

Asegúrate de tener los siguientes paquetes instalados:

- `streamlit`
- `fastapi`
- `requests`
- `pandas`
- `openpyxl`
- `uvicorn` (para ejecutar FastAPI)
- Otros paquetes necesarios (ver `requirements.txt` para detalles)

## Instalación

1. **Crear y activar un entorno virtual (opcional pero recomendado):**

   ```bash
   python -m venv env
   source env/bin/activate  # En Windows: env\Scripts\activate
    ```

1. **Instalar las dependencias:**
   ```bash
   pip install -r requirements.txt
    ```

## Ejecutar la Aplicación

1. **Interfaz de Usuario (Streamlit):**

Para iniciar la interfaz de usuario de Streamlit, navega a la carpeta front y ejecuta el archivo `homepage.py`

   ```bash
  cd front
  streamlit run homepage.py
  ```
Esto abrirá la aplicación en tu navegador predeterminado.

2. **Servicio de Backend (FastAPI):**

Para iniciar el servicio de backend de FastAPI, navega a la carpeta back y ejecuta el archivo `main.py` usando Uvicorn:

   ```bash
  cd back
  uvicorn main:app --reload
  ```
Esto iniciará el servidor en http://127.0.0.1:8000, y podrás interactuar con la API de FastAPI en esa URL.

## Uso

1. **Interfaz de Usuario (Streamlit):**
- Abre la aplicación de Streamlit en tu navegador.
- Usa la interfaz para gestionar contactos, escribir mensajes y previsualizar la lista de destinatarios.

2. **Servicio de Backend (FastAPI):**
- La API estará disponible en http://127.0.0.1:8000.
- Puedes consultar la documentación automática en http://127.0.0.1:8000/docs.

## Contribuciones

Si deseas contribuir a este proyecto, por favor sigue las prácticas comunes de contribución y realiza un pull request.