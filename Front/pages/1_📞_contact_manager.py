from streamlit_option_menu import option_menu
import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Contact manager",
    page_icon="📞",
)

selected = option_menu(
    menu_title=None,
    options=["Todos", "Nuevos", "Ventas", "Baneados"],
    icons=["collection", "clipboard2-plus", "basket2", "cone-striped"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

archivo_excel = os.path.join('pages', 'resources', 'contacts.xlsx')

if not os.path.exists(archivo_excel):
    df_dummy = pd.DataFrame({
        'Nombre': ['Juan Perez', 'Maria Garcia', 'Carlos Lopez'],
        'Número': ['555-1234', '555-5678', '555-8765'],
        'Etiqueta': ['Nuevos', 'Ventas', 'Baneados'],
        'Seleccionado': ['SI', 'NO', 'NO'],
    })
    df_dummy.to_excel(archivo_excel, index=False)

def cargar_contactos(archivo_excel):
    return pd.read_excel(archivo_excel)

def guardar_contactos(df, archivo_excel):
    df.to_excel(archivo_excel, index=False)

# Definir las etiquetas disponibles
etiquetas = ["Nuevos", "Ventas", "Baneados"]
seleccionado = ["SI", "NO"]

# Cargar los contactos y almacenarlos en el estado de la sesión
if "df_contactos" not in st.session_state:
    st.session_state.df_contactos = cargar_contactos(archivo_excel)

def actualizar_dataframe(df):
    st.session_state.df_contactos = df
    guardar_contactos(df, archivo_excel)

def marcar_como_seleccionado(filtrar_por=None):
    df = st.session_state.df_contactos.copy()
    if filtrar_por:
        df.loc[df['Etiqueta'] == filtrar_por, 'Seleccionado'] = 'SI'
    else:
        df['Seleccionado'] = 'SI'
    actualizar_dataframe(df)
    st.success("Todos los contactos han sido marcados como seleccionados.")

def mostrar_contactos(filtrar_por=None):
    df = st.session_state.df_contactos.copy()

    if filtrar_por:
        if st.button(f"Marcar todos los '{filtrar_por}' como seleccionados"):
            marcar_como_seleccionado(filtrar_por)
            df = st.session_state.df_contactos.copy()

        df_filtrado = df[df['Etiqueta'] == filtrar_por]
        st.write(f"### Contactos con la etiqueta '{filtrar_por}'")
        st.dataframe(df_filtrado)

        st.write("---")
        
        df_filtrado_seleccionado = df_filtrado[df_filtrado['Seleccionado'] == 'SI']
        st.write(f"### Contactos elegidos para enviar mensajes con la etiqueta '{filtrar_por}'")
        st.dataframe(df_filtrado_seleccionado)
    else:
        if st.button(f"Marcar todos como seleccionados"):
            marcar_como_seleccionado()
            df = st.session_state.df_contactos.copy()

        st.title(f"{selected} los contactos")
        for i in range(len(df)):
            contacto = df.iloc[i]
            st.write(f"**Nombre:** {contacto['Nombre']}")
            st.write(f"**Número:** {contacto['Número']}")

            etiqueta_seleccionada = st.selectbox(
                f"Etiqueta para {contacto['Nombre']}",
                etiquetas,
                index=etiquetas.index(contacto['Etiqueta']),
                key=f"selectbox_etiqueta_{i}"
            )
            df.at[i, 'Etiqueta'] = etiqueta_seleccionada

            seleccionado_estado = st.selectbox(
                f"Seleccionado para {contacto['Nombre']}",
                seleccionado,
                index=seleccionado.index(contacto['Seleccionado']),
                key=f"selectbox_seleccionado_{i}"
            )
            df.at[i, 'Seleccionado'] = seleccionado_estado
            st.write("---")
        
        actualizar_dataframe(df)
        
        df_selected = df[df['Seleccionado'] == 'SI']
        st.write(f"### Contactos elegidos para enviar mensajes")
        st.dataframe(df_selected)

if selected == "Todos":
    mostrar_contactos()
else:
    mostrar_contactos(filtrar_por=selected)