
import streamlit as st
import pandas as pd
import sqlite3
import os
from datetime import datetime

# Cargar datos
EXCEL_PATH = "Base_Tareas_Operativas_Patria.xlsx"
DB_PATH = "bitacora_operapatria.db"

st.set_page_config(page_title="Bitácora Operativa", layout="wide")

st.title("Bitácora Operativa - Plaza Patria / Vía Viva")

# Cargar datos desde Excel
df = pd.read_excel(EXCEL_PATH)

# Limpiar nombres de columnas
df.columns = df.columns.astype(str)
df.columns = df.columns.str.strip().str.replace(r"[\n\r\t]+", "", regex=True).str.lower()

# Sidebar
plazas = ["Todas"] + sorted(df["plaza"].dropna().unique().tolist())
plaza_select = st.sidebar.selectbox("Selecciona plaza", plazas)

if plaza_select != "Todas":
    df = df[df["plaza"] == plaza_select]

# Mostrar datos
st.dataframe(df)

# Conexión a SQLite para tareas completadas (opcional)
if os.path.exists(DB_PATH):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS tareas_cumplidas (id_tarea TEXT PRIMARY KEY, fecha_cumplimiento TEXT)")
    conn.commit()

    st.sidebar.markdown("### Marcar tarea como cumplida")
    tarea_id = st.sidebar.text_input("ID de tarea")
    if st.sidebar.button("Marcar cumplida"):
        fecha = datetime.today().strftime("%Y-%m-%d")
        try:
            cur.execute("INSERT OR REPLACE INTO tareas_cumplidas (id_tarea, fecha_cumplimiento) VALUES (?, ?)", (tarea_id, fecha))
            conn.commit()
            st.success(f"Tarea {tarea_id} marcada como cumplida")
        except Exception as e:
            st.error(f"Error: {e}")
    conn.close()
