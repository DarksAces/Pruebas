import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
import os
import re

# --- CONFIGURACIÓN ---
KEY_PATH = "serviceAccountKeyJovi.json" 

# Tu bucket
BUCKET_NAME = "jovi-45c79.firebasestorage.app"

# La carpeta que quieres descargar
SOURCE_FOLDER = "stop_photos" 

# Carpeta local donde se guardarán (directo al dataset de entrenamiento para integrarlo)
# Lo mandamos a una carpeta temporal o directo a 'dataset/train/firebase_jovi' para que el script de limpieza lo pille
LOCAL_FOLDER = "dataset/train/firebase_jovi" 

def sanitize_filename(name):
    # Reemplaza caracteres prohibidos en Windows (< > : " / \ | ? *) por guión bajo
    return re.sub(r'[<>:"/\\|?*]', '_', name)

def download_from_firebase():
    print("--- DESCARGADOR DE FIREBASE (JOVI) ---")
    
    if not os.path.exists(KEY_PATH):
        print(f"❌ ERROR: No encuentro el archivo de llave '{KEY_PATH}'.")
        return

    try:
        # Iniciar sesión
        cred = credentials.Certificate(KEY_PATH)
        # Check if app already initialized to avoid errors
        try:
            app = firebase_admin.get_app()
        except ValueError:
            app = firebase_admin.initialize_app(cred, {
                'storageBucket': BUCKET_NAME
            })
        
        bucket = storage.bucket()
        print(f"Conectado a: {BUCKET_NAME}")
        print(f"Buscando archivos en: {SOURCE_FOLDER}/ ...")

        blobs = bucket.list_blobs(prefix=SOURCE_FOLDER)
        
        if not os.path.exists(LOCAL_FOLDER):
            os.makedirs(LOCAL_FOLDER)
            print(f"Carpeta '{LOCAL_FOLDER}' creada.")

        count = 0
        for blob in blobs:
            if blob.name.endswith('/'): 
                continue 
                
            original_filename = os.path.basename(blob.name)
            if not original_filename:
                continue

            # Sanitize name
            safe_name = sanitize_filename(original_filename)
            local_path = os.path.join(LOCAL_FOLDER, safe_name)
            
            # Skip if exists
            if os.path.exists(local_path):
                 print(f"Saltando (ya existe): {safe_name}")
                 continue

            print(f"Descargando: {safe_name}")
            blob.download_to_filename(local_path)
            count += 1

        print(f"\n✅ ¡ÉXITO! {count} imágenes descargadas en '{LOCAL_FOLDER}'.")

    except Exception as e:
        print(f"\n❌ OCURRIÓ UN ERROR: {e}")

if __name__ == "__main__":
    download_from_firebase()
