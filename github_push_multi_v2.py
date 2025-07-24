import os
from github import Github
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not GITHUB_TOKEN:
    raise ValueError("Token de GitHub no encontrado. Asegúrate de tener un archivo .env con GITHUB_TOKEN=...")

# Configura el nombre del repositorio y el directorio local
REPO_NAME = "doplaza/BitacoraOperaPatria"
LOCAL_DIR = "/Users/ra/Documents/PP/WADMIN"

# Inicializa la conexión a GitHub
g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)

# Archivos a ignorar
archivos_ignorados = [".env", ".DS_Store", "__pycache__"]
extensiones_ignoradas = [".pyc"]

# Subir archivos
for root, dirs, files in os.walk(LOCAL_DIR):
    for filename in files:
        if filename in archivos_ignorados or any(filename.endswith(ext) for ext in extensiones_ignoradas):
            continue

        filepath = os.path.join(root, filename)
        relative_path = os.path.relpath(filepath, LOCAL_DIR)

        # Verifica que el archivo no esté vacío
        if os.path.getsize(filepath) == 0:
            print(f"⚠️ Archivo vacío (omitido): {relative_path}")
            continue

        with open(filepath, "rb") as f:
            content = f.read()

        print(f"📦 Procesando archivo: {relative_path} ({len(content)} bytes)")
        commit_message = f"Archivo actualizado: {relative_path}"

        try:
            # Si ya existe, lo actualiza
            contents = repo.get_contents(relative_path)
            repo.update_file(contents.path, commit_message, content, contents.sha)
            print(f"✅ Archivo actualizado: {relative_path}")
        except Exception:
            try:
                # Si no existe, lo crea
                repo.create_file(relative_path, commit_message, content)
                print(f"🆕 Archivo creado: {relative_path}")
            except Exception as e:
                print(f"❌ Error al subir {relative_path}: {e}")

