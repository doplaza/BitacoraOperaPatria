
import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(page_title="Bitácora Operativa", layout="wide")

# Función para cargar los datos
def load_data():
    conn = sqlite3.connect("bitacora_operapatria_con_id.db")
    df = pd.read_sql_query("SELECT * FROM tareas", conn)
    conn.close()
    return df

df = load_data()

# Sidebar - Filtros
st.sidebar.title("Filtros")

# Aseguramos que el DataFrame tenga datos
if not df.empty:
    plazas = ["Todas"] + sorted(df["plaza"].dropna().unique().tolist())
    areas = ["Todas"] + sorted(df["area"].dropna().unique().tolist())
    estatuses = ["Todos"] + sorted(df["estatus"].dropna().unique().tolist())

    plaza = st.sidebar.selectbox("Plaza", plazas)
    area = st.sidebar.selectbox("Área", areas)
    estatus = st.sidebar.selectbox("Estatus", estatuses)

    # Aplicar filtros
    if plaza != "Todas":
        df = df[df["plaza"] == plaza]
    if area != "Todas":
        df = df[df["area"] == area]
    if estatus != "Todos":
        df = df[df["estatus"] == estatus]
else:
    st.sidebar.warning("No hay datos disponibles para mostrar filtros.")

# Mostrar tabla
st.title("Bitácora Operativa")
st.dataframe(df, use_container_width=True)
