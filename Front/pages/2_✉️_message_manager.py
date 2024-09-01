import streamlit as st
import pandas as pd
import os
import requests
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Message Manager",
    page_icon="✉️",
)

archivo_excel = os.path.join('pages', 'resources', 'contacts.xlsx')
archivo_csv = os.path.join('pages', 'resources', 'contador_mensajes.csv')

def cargar_contactos_seleccionados(archivo_excel):
    df = pd.read_excel(archivo_excel)
    df_seleccionados = df[df['Seleccionado'] == 'SI']
    return df_seleccionados

def registrar_mensaje(numero, archivo_csv='contador_mensajes.csv'):
    # Cargar el CSV o crear uno nuevo si no existe
    try:
        df = pd.read_csv(archivo_csv)
    except FileNotFoundError:
        df = pd.DataFrame(columns=['Número de Teléfono', 'Fecha y Hora del Mensaje', 'Mensaje Cobrado'])

    # Obtener la fecha y hora actual
    ahora = datetime.now()

    # Filtrar por el número de teléfono y mensajes cobrados
    df_numero_cobrado = df[(df['Número de Teléfono'] == numero) & (df['Mensaje Cobrado'] == 'SI')]

    # Verificar si el último mensaje cobrado fue hace más de 24 horas
    mensaje_cobrado = 'SI'
    if not df_numero_cobrado.empty:
        ultima_fecha_cobrado = pd.to_datetime(df_numero_cobrado['Fecha y Hora del Mensaje'].iloc[-1])
        if ahora - ultima_fecha_cobrado < timedelta(hours=24):
            mensaje_cobrado = 'NO'

    # Crear DataFrame para el nuevo mensaje
    nuevo_mensaje_df = pd.DataFrame({
        'Número de Teléfono': [numero],
        'Fecha y Hora del Mensaje': [ahora],
        'Mensaje Cobrado': [mensaje_cobrado]
    })

    # Concatenar el nuevo mensaje con el DataFrame existente
    df = pd.concat([df, nuevo_mensaje_df], ignore_index=True)

    # Guardar el CSV actualizado
    df.to_csv(archivo_csv, index=False)

def calcular_costo_total(archivo_csv='contador_mensajes.csv', costo_por_mensaje=0.04):
    df = pd.read_csv(archivo_csv)
    total_mensajes_cobrados = df[df['Mensaje Cobrado'] == 'SI'].shape[0]
    costo_total = total_mensajes_cobrados * costo_por_mensaje
    return costo_total

df_seleccionados = cargar_contactos_seleccionados(archivo_excel)

mensaje = st.text_area("Escribe el mensaje que quieres enviar:")

if st.button("Enviar mensajes"):
    if mensaje.strip() == "":
        st.warning("Por favor, escribe un mensaje antes de enviar.")
    elif df_seleccionados.empty:
        st.warning("No hay contactos seleccionados para enviar el mensaje.")
    else:
        mensajes = {row['Número']: mensaje for _, row in df_seleccionados.iterrows()}

        respuesta = requests.post("http://127.0.0.1:8000/enviar_mensaje/", json=mensajes)

        if respuesta.status_code == 200:
            for numero in mensajes.keys():
                registrar_mensaje(numero, archivo_csv)
            
            st.success("Mensajes enviados correctamente.")
        else:
            st.error("Hubo un error al enviar los mensajes.")

costo_total = calcular_costo_total(archivo_csv)
st.write(f"**Costo total estimado hasta ahora:** ${costo_total:.2f}")

if not df_seleccionados.empty:
    st.write("### Lista de contactos seleccionados:")
    st.dataframe(df_seleccionados[['Nombre', 'Número']])
else:
    st.write("No hay contactos seleccionados.")
