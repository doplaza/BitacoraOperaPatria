
import streamlit as st
import pandas as pd
import sqlite3
import os

# Configuración general
st.set_page_config(page_title="Bitácora Operativa Patria", layout="wide")
st.title("📋 Bitácora Operativa de Plaza Patria")

DB_PATH = "bitacora_operapatria_con_id.db"

# Función para conectar a SQLite
def get_connection(path=DB_PATH):
    return sqlite3.connect(path)

# Cargar datos actuales
def load_data():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM tareas", conn)
    conn.close()
    return df

# Actualizar campos desde Excel maestro
def update_from_excel(uploaded_file):
    try:
        df_update = pd.read_excel(uploaded_file)
        if "id_tarea" not in df_update.columns:
            st.error("El archivo debe contener la columna 'id_tarea'.")
            return None

        with get_connection() as conn:
            df_actual = pd.read_sql_query("SELECT * FROM tareas", conn)
            df_actual.set_index("id_tarea", inplace=True)

            updated_count = 0
            for _, row in df_update.iterrows():
                id_tarea = row["id_tarea"]
                if id_tarea in df_actual.index:
                    for campo in ["Responsable", "Fecha Compromiso", "Fecha Cumplimiento"]:
                        if campo in row and pd.notna(row[campo]):
                            df_actual.at[id_tarea, campo] = row[campo]
                            updated_count += 1

            df_actual.reset_index(inplace=True)
            df_actual.to_sql("tareas", conn, if_exists="replace", index=False)

        st.success(f"Actualización completa. Se actualizaron {updated_count} campos.")
    except Exception as e:
        st.exception(e)

# Mostrar datos actuales
st.subheader("🔎 Datos actuales")
df = load_data()
st.dataframe(df, use_container_width=True)

# Subida de archivo maestro para actualización
st.subheader("⬆️ Cargar Excel maestro")
uploaded_file = st.file_uploader("Selecciona el archivo Excel para actualizar tareas", type=["xlsx"])
if uploaded_file:
    with st.expander("📄 Vista previa del archivo cargado"):
        df_preview = pd.read_excel(uploaded_file)
        st.dataframe(df_preview, use_container_width=True)

    if st.button("✅ Actualizar base de datos"):
        update_from_excel(uploaded_file)
