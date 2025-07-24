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

# Archivos a subir (todos los archivos del directorio excepto los ignorados)
archivos_ignorados = [".env", ".DS_Store", "__pycache__"]
extensiones_ignoradas = [".pyc"]

# Carga los archivos locales
for root, dirs, files in os.walk(LOCAL_DIR):
    for filename in files:
        if filename in archivos_ignorados or any(filename.endswith(ext) for ext in extensiones_ignoradas):
            continue

        filepath = os.path.join(root, filename)
        relative_path = os.path.relpath(filepath, LOCAL_DIR)
        with open(filepath, "rb") as f:
            content = f.read()

        commit_message = f"Archivo actualizado: {relative_path}"

        try:
            # Revisa si ya existe el archivo
            contents = repo.get_contents(relative_path)
            repo.update_file(contents.path, commit_message, content, contents.sha)
            print(f"Archivo actualizado: {relative_path}")
        except Exception as e:
            try:
                repo.create_file(relative_path, commit_message, content)
                print(f"Archivo creado: {relative_path}")
            except Exception as e:
                print(f"Error al subir {relative_path}: {e}")
