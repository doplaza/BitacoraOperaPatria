
import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
import os

# --- Configuracion general ---
st.set_page_config(page_title="Bitácora Operativa", layout="wide")
PASSWORD = "operapatria2025"
DB_PATH = "bitacora_operapatria.db"

# --- Autenticacion ---
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    with st.form("login"):
        st.title("🔐 Acceso a Bitácora Operativa")
        password = st.text_input("Contraseña", type="password")
        submitted = st.form_submit_button("Ingresar")
        if submitted:
            if password == PASSWORD:
                st.session_state.auth = True
            else:
                st.error("Contraseña incorrecta")
    st.stop()

# --- Cargar base de datos ---
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
df = pd.read_sql_query("SELECT rowid, * FROM tareas", conn)

# --- Filtros ---
st.sidebar.title("Filtros")
plaza = st.sidebar.selectbox("Plaza", ["Todas"] + sorted(df["Área"].unique().tolist()))
area = st.sidebar.selectbox("Área", ["Todas"] + sorted(df["Área"].dropna().unique().tolist()))
estatus = st.sidebar.selectbox("Estatus", ["Todos", "Pendiente", "En proceso", "Completado", "Vencido"])

# --- Aplicar filtros ---
if plaza != "Todas":
    df = df[df["Área"] == plaza]
if area != "Todas":
    df = df[df["Área"] == area]
if estatus != "Todos":
    df = df[df["Estatus"] == estatus]

# --- Mostrar tabla con colores de vencimiento ---
def color_row(row):
    try:
        if row["Estatus"] != "Completado" and pd.to_datetime(row["fecha_compromiso"]) < datetime.now():
            return ["background-color: #ffcccc"] * len(row)
        else:
            return [""] * len(row)
    except:
        return [""] * len(row)

st.title("📋 Bitácora Operativa - Vista General")
st.dataframe(df.style.apply(color_row, axis=1), use_container_width=True)

# --- Formulario para actualizar tarea ---
st.markdown("---")
st.subheader("✏️ Actualizar tarea")
selected_id = st.selectbox("Selecciona el ID de tarea a actualizar", df["rowid"])
selected_task = df[df["rowid"] == selected_id].iloc[0]

with st.form("update_form"):
    nuevo_estatus = st.selectbox("Nuevo estatus", ["Pendiente", "En proceso", "Completado", "Vencido"],
                                 index=["Pendiente", "En proceso", "Completado", "Vencido"].index(selected_task["Estatus"])
                                 if selected_task["Estatus"] in ["Pendiente", "En proceso", "Completado", "Vencido"] else 0)
    nueva_fecha = st.date_input("Fecha de cumplimiento", value=datetime.now())
    observaciones = st.text_area("Observaciones", value=selected_task["observaciones"] if pd.notna(selected_task["observaciones"]) else "")
    evidencia_files = st.file_uploader("Sube archivos de evidencia (puedes subir varios)", accept_multiple_files=True)
    submit_update = st.form_submit_button("Guardar cambios")

    if submit_update:
        folder = f"evidencias/tarea_{selected_id}"
        os.makedirs(folder, exist_ok=True)
        paths = []
        for file in evidencia_files:
            path = os.path.join(folder, file.name)
            with open(path, "wb") as f:
                f.write(file.getbuffer())
            paths.append(path)

        evidencia_str = "; ".join(paths)
        cursor.execute("""
            UPDATE tareas
            SET estatus = ?, fecha_cumplimiento = ?, observaciones = ?, evidencia = ?
            WHERE rowid = ?
        """, (nuevo_estatus, nueva_fecha.strftime("%Y-%m-%d"), observaciones, evidencia_str, selected_id))
        conn.commit()
        st.success("Tarea actualizada correctamente.")
