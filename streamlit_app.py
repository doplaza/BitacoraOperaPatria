
import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(page_title="Bitácora Operativa", layout="wide")

# Autenticación básica
def check_password():
    def password_entered():
        if st.session_state["password"] == "operapatria2025":
            st.session_state["authenticated"] = True
        else:
            st.session_state["authenticated"] = False
            st.session_state["password"] = ""
    if "authenticated" not in st.session_state:
        st.text_input("Contraseña", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["authenticated"]:
        st.text_input("Contraseña", type="password", on_change=password_entered, key="password")
        return False
    else:
        return True

if not check_password():
    st.stop()

# Cargar datos
def load_data():
    conn = sqlite3.connect("bitacora_operapatria.db")
    df = pd.read_sql_query("SELECT * FROM tareas", conn)
    conn.close()
    return df

df = load_data()

# Filtros en barra lateral
plazas = ["Todas"] + sorted(df["Plaza"].dropna().unique().tolist())
areas = ["Todas"] + sorted(df["Área"].dropna().unique().tolist())
estatus = ["Todos"] + sorted(df["Estatus"].dropna().unique().tolist())

st.sidebar.title("Filtros")
plaza_sel = st.sidebar.selectbox("Plaza", plazas)
area_sel = st.sidebar.selectbox("Área", areas)
estatus_sel = st.sidebar.selectbox("Estatus", estatus)

# Aplicar filtros
if plaza_sel != "Todas":
    df = df[df["Plaza"] == plaza_sel]
if area_sel != "Todas":
    df = df[df["Área"] == area_sel]
if estatus_sel != "Todos":
    df = df[df["Estatus"] == estatus_sel]

# Mostrar tabla
st.title("Bitácora Operativa")
st.dataframe(df, use_container_width=True)
