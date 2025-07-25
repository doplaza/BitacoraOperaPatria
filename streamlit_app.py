import streamlit as st
import pandas as pd
import sqlite3
import os
from datetime import datetime

# Rutas de archivos
EXCEL_PATH = "Base_Tareas_Operativas_Patria.xlsx"
DB_PATH = "bitacora_operapatria.db"

st.set_page_config(page_title="Bitácora Operativa", layout="wide")
st.title("Bitácora Operativa - Plaza Patria / Vía Viva")

# Cargar archivo Excel
def cargar_datos_excel(path):
    df = pd.read_excel(path)
    df.columns = df.columns.astype(str)
    df.columns = df.columns.str.strip().str.replace(r"[\n\r\t]+", "", regex=True).str.lower()
    return df

# Subida de nuevo archivo Excel
st.sidebar.markdown("### 📂 Subir nuevo Excel")
nuevo_excel = st.sidebar.file_uploader("Reemplazar archivo de tareas", type=["xlsx"])
if nuevo_excel:
    with open(EXCEL_PATH, "wb") as f:
        f.write(nuevo_excel.read())
    st.sidebar.success("Archivo reemplazado correctamente. Recarga la app para ver los cambios.")

# Cargar datos
df = cargar_datos_excel(EXCEL_PATH)

# Validación de columna plaza
if "plaza" not in df.columns:
    st.error("❌ La columna 'plaza' no está presente en el archivo Excel.")
    st.stop()

# Filtros
with st.sidebar:
    st.markdown("### 🔎 Filtros de búsqueda")

    plazas = ["Todas"] + sorted(df["plaza"].dropna().unique().tolist())
    plaza_select = st.selectbox("Selecciona plaza", plazas)

    responsables = ["Todos"] + sorted(df["responsable"].dropna().unique().tolist())
    responsable_select = st.selectbox("Selecciona responsable", responsables)

    areas = ["Todas"] + sorted(df["área"].dropna().unique().tolist())
    area_select = st.selectbox("Selecciona área", areas)

    frecuencias = ["Todas"] + sorted(df["frecuencia"].dropna().unique().tolist())
    frecuencia_select = st.selectbox("Selecciona frecuencia", frecuencias)

    estatuses = ["Todos"] + sorted(df["estatus"].dropna().unique().tolist())
    estatus_select = st.selectbox("Selecciona estatus", estatuses)

# Aplicar filtros
if plaza_select != "Todas":
    df = df[df["plaza"] == plaza_select]
if responsable_select != "Todos":
    df = df[df["responsable"] == responsable_select]
if area_select != "Todas":
    df = df[df["área"] == area_select]
if frecuencia_select != "Todas":
    df = df[df["frecuencia"] == frecuencia_select]
if estatus_select != "Todos":
    df = df[df["estatus"] == estatus_select]

# Mostrar tabla
st.dataframe(df, use_container_width=True)

# Registrar cumplimiento de tareas
if os.path.exists(DB_PATH):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS tareas_cumplidas (id_tarea TEXT PRIMARY KEY, fecha_cumplimiento TEXT)")
    conn.commit()

    st.sidebar.markdown("### ✅ Marcar tareas como cumplidas")
    tareas_text = st.sidebar.text_area("IDs de tareas (separadas por coma o salto de línea)", height=100)
    marcar_btn = st.sidebar.button("Marcar como cumplidas")

    if marcar_btn and tareas_text.strip():
        ids = [t.strip() for t in tareas_text.replace("\n", ",").split(",") if t.strip()]
        fecha = datetime.today().strftime("%Y-%m-%d")
        errores = []
        for tarea_id in ids:
            try:
                cur.execute("INSERT OR REPLACE INTO tareas_cumplidas (id_tarea, fecha_cumplimiento) VALUES (?, ?)", (tarea_id, fecha))
            except Exception as e:
                errores.append(tarea_id)
        conn.commit()
        if errores:
            st.sidebar.warning(f"No se pudieron registrar estas tareas: {', '.join(errores)}")
        else:
            st.sidebar.success(f"Se registraron correctamente {len(ids)} tareas.")
    conn.close()
