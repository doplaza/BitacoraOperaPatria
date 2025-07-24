import streamlit as st
import pandas as pd
import sqlite3
import os

# Cargar datos
archivo = "Base_Tareas_Operativas_Patria.xlsx"
if not os.path.exists(archivo):
    st.error(f"Archivo {archivo} no encontrado.")
    st.stop()

df = pd.read_excel(archivo)

# Normaliza los nombres de las columnas
df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

# Revisa que esté la columna 'plaza'
if "plaza" not in df.columns:
    st.error("La columna 'plaza' no se encuentra en el archivo.")
    st.write("Columnas encontradas:", df.columns.tolist())
    st.stop()

# Filtros
plazas = ["Todas"] + sorted(df["plaza"].dropna().unique().tolist())
plaza_seleccionada = st.sidebar.selectbox("Selecciona la plaza", plazas)

# Aplica el filtro
if plaza_seleccionada != "Todas":
    df = df[df["plaza"] == plaza_seleccionada]

st.title("Bitácora Opera Patria")
st.dataframe(df)
