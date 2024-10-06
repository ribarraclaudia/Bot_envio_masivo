import schedule
import time
import threading
import streamlit as st
import pandas as pd
import os
import requests
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Message Manager",
    page_icon="✉️",
)

archivo_excel_contactos = os.path.join('pages', 'resources', 'contacts.xlsx')
archivo_csv_contador = os.path.join('pages', 'resources', 'contador_mensajes.csv')
archivo_excel_mensajes = os.path.join('pages', 'resources', 'mensajes_predefinidos.xlsx')
archivo_csv_mensajes_programados = os.path.join('pages', 'resources', 'mensajes_programados.csv')

def cargar_contactos_seleccionados(archivo_excel):
    df = pd.read_excel(archivo_excel)
    df_seleccionados = df[df['Seleccionado'] == 'SI']
    return df_seleccionados

def cargar_mensajes_predefinidos(archivo_excel):
    df = pd.read_excel(archivo_excel)
    return df

def registrar_mensaje(numero, archivo_csv='contador_mensajes.csv'):
    try:
        df = pd.read_csv(archivo_csv)
    except FileNotFoundError:
        df = pd.DataFrame(columns=['Número de Teléfono', 'Fecha y Hora del Mensaje', 'Mensaje Cobrado'])

    ahora = datetime.now()
    df_numero_cobrado = df[(df['Número de Teléfono'] == numero) & (df['Mensaje Cobrado'] == 'SI')]

    mensaje_cobrado = 'SI'
    if not df_numero_cobrado.empty:
        ultima_fecha_cobrado = pd.to_datetime(df_numero_cobrado['Fecha y Hora del Mensaje'].iloc[-1])
        if ahora - ultima_fecha_cobrado < timedelta(hours=24):
            mensaje_cobrado = 'NO'

    nuevo_mensaje_df = pd.DataFrame({
        'Número de Teléfono': [numero],
        'Fecha y Hora del Mensaje': [ahora],
        'Mensaje Cobrado': [mensaje_cobrado]
    })

    df = pd.concat([df, nuevo_mensaje_df], ignore_index=True)
    df.to_csv(archivo_csv, index=False)

def calcular_costo_total(archivo_csv='contador_mensajes.csv', costo_por_mensaje=0.04):
    df = pd.read_csv(archivo_csv)
    total_mensajes_cobrados = df[df['Mensaje Cobrado'] == 'SI'].shape[0]
    costo_total = total_mensajes_cobrados * costo_por_mensaje
    return costo_total

# Enviar mensajes inmediatamente
def enviar_mensajes_inmediato(mensajes):
    respuesta = requests.post("http://127.0.0.1:8000/enviar_mensaje/", json=mensajes)

    if respuesta.status_code == 200:
        for numero in mensajes.keys():
            registrar_mensaje(numero, archivo_csv_contador)
        st.success("Mensajes enviados correctamente.")
    else:
        st.error("Hubo un error al enviar los mensajes.")


# Guardar mensajes programados en una lista de espera (archivo CSV)
def guardar_mensaje_programado(df_mensajes_programados, mensaje, hora_futura):
    df_mensajes_programados = pd.concat([df_mensajes_programados, pd.DataFrame({
        'Número': [row['Número'] for _, row in df_seleccionados.iterrows()],
        'Mensaje': [mensaje] * len(df_seleccionados),
        'Hora Programada': [hora_futura] * len(df_seleccionados)
    })], ignore_index=True)
    df_mensajes_programados.to_csv(archivo_csv_mensajes_programados, index=False)
    st.success(f"Mensajes programados para las {hora_futura}.")

# Cargar los mensajes programados desde un archivo CSV
def cargar_mensajes_programados(archivo_csv):
    if os.path.exists(archivo_csv):
        df = pd.read_csv(archivo_csv)
    else:
        df = pd.DataFrame(columns=['Número', 'Mensaje', 'Hora Programada'])
    return df


# Verificar y enviar mensajes programados
def verificar_mensajes_programados(df_mensajes_programados):
    ahora = datetime.now()
    df_enviar = df_mensajes_programados[pd.to_datetime(df_mensajes_programados['Hora Programada']) <= ahora]

    for _, row in df_enviar.iterrows():
        mensajes = {row['Número']: row['Mensaje']}
        enviar_mensajes_inmediato(mensajes)

    # Eliminar los mensajes enviados de la lista
    df_mensajes_programados = df_mensajes_programados[pd.to_datetime(df_mensajes_programados['Hora Programada']) > ahora]
    df_mensajes_programados.to_csv(archivo_csv_mensajes_programados, index=False)  # Actualizar el archivo sin los mensajes enviados


# Función para programar el envío de mensajes
def programar_envio_mensajes(hora_futura, mensaje):
    df_mensajes_programados = cargar_mensajes_programados(archivo_csv_mensajes_programados)
    guardar_mensaje_programado(df_mensajes_programados, mensaje, hora_futura)


# Ejecutar la verificación de mensajes programados en segundo plano
def run_schedule():
    while True:
        df_mensajes_programados = cargar_mensajes_programados(archivo_csv_mensajes_programados)
        verificar_mensajes_programados(df_mensajes_programados)
        time.sleep(60)  # Verificar cada minuto


# Iniciar el hilo para la verificación continua de mensajes programados
threading.Thread(target=run_schedule, daemon=True).start()

df_seleccionados = cargar_contactos_seleccionados(archivo_excel_contactos)
df_mensajes = cargar_mensajes_predefinidos(archivo_excel_mensajes)

clave_seleccionada = st.selectbox("Selecciona un mensaje predefinido:", df_mensajes['Clave'])

mensaje_seleccionado = df_mensajes[df_mensajes['Clave'] == clave_seleccionada]['Mensaje'].values[0]

mensaje = st.text_area("Escribe el mensaje que quieres enviar:", value=mensaje_seleccionado)

# Usar st.session_state para almacenar la hora por defecto solo una vez
if "hora_futura_por_defecto" not in st.session_state:
    st.session_state.hora_futura_por_defecto = (datetime.now() + timedelta(minutes=10)).time()

# Opciones para envío
opcion_envio = st.radio("Selecciona una opción para el envío del mensaje:", ("Enviar ahora", "Programar para más tarde"))

if opcion_envio == "Enviar ahora":
    if st.button("Enviar mensajes ahora"):
        if mensaje.strip() == "":
            st.warning("Por favor, escribe un mensaje antes de enviar.")
        elif df_seleccionados.empty:
            st.warning("No hay contactos seleccionados para enviar el mensaje.")
        else:
            mensajes = {row['Número']: mensaje for _, row in df_seleccionados.iterrows()}
            enviar_mensajes_inmediato(mensajes)

elif opcion_envio == "Programar para más tarde":
    # Elegir hora y fecha para programar
    hora_futura = st.time_input("Hora de envío programado", st.session_state.hora_futura_por_defecto)  # Usamos la hora almacenada en session_state
    fecha_futura = st.date_input("Fecha de envío programado", datetime.now().date())
    hora_futura_completa = datetime.combine(fecha_futura, hora_futura)

    if st.button("Programar envío de mensajes"):
        if mensaje.strip() == "":
            st.warning("Por favor, escribe un mensaje antes de programar.")
        elif df_seleccionados.empty:
            st.warning("No hay contactos seleccionados para enviar el mensaje.")
        else:
            programar_envio_mensajes(hora_futura_completa, mensaje)

costo_total = calcular_costo_total(archivo_csv_contador)
st.write(f"**Costo total estimado hasta ahora:** ${costo_total:.2f}")

if not df_seleccionados.empty:
    st.write("### Lista de contactos seleccionados:")
    st.dataframe(df_seleccionados[['Nombre', 'Número']])
else:
    st.write("No hay contactos seleccionados.")