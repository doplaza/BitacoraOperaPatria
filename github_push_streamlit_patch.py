from github import Github
import os
from dotenv import load_dotenv
import re

# Cargar token de entorno
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Configura tu repositorio y archivo
REPO_NAME = "doplaza/BitacoraOperaPatria"
FILE_PATH = "BitacoraOperaPatria/streamlit_app.py"
LOCAL_PATH = f"/Users/ra/Documents/PP/WADMIN/{FILE_PATH}"
COMMIT_MESSAGE = "🔧 Limpieza de columnas para evitar errores KeyError por 'Plaza'"

# Inicializa conexión a GitHub
g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)

# Lee el archivo local y hace la modificación
with open(LOCAL_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# Reemplazo seguro
new_code = '''
# Limpia nombres de columnas
df.columns = df.columns.str.strip().str.lower()

if "plaza" not in df.columns:
    st.error("La columna 'plaza' no fue encontrada en el archivo.")
    st.stop()

plazas = ["Todas"] + sorted(df["plaza"].dropna().unique().tolist())
'''

content = re.sub(
    r'plazas\s*=\s*\["Todas"\]\s*\+\s*sorted\(df\["Plaza"\]\.dropna\(\)\.unique\(\)\.tolist\(\)\)',
    new_code,
    content
)

# Sube al repositorio
remote_file = repo.get_contents(FILE_PATH)
repo.update_file(FILE_PATH, COMMIT_MESSAGE, content, remote_file.sha)
print(f"✅ Archivo actualizado correctamente: {FILE_PATH}")
