import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
import os
import sys
from PIL import Image
import io

# --- CONFIGURACIÓN ---
KEY_PATH = "redtrain-f6b30-firebase-adminsdk-fbsvc-59f4497939.json"
BUCKET_NAME = "redtrain-f6b30.firebasestorage.app" # Asumed bucket name based on project ID
DATASET_ROOT = "dataset"
REMOTE_FOLDER = "dataset_v3_compressed"

def compress_image(image_path, quality=60, max_size=(1024, 1024)):
    try:
        with Image.open(image_path) as img:
            # Convert to RGB if necessary (e.g. RGBA)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            
            # Resize if too big
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Save to memory buffer
            buffer = io.BytesIO()
            img.save(buffer, format="JPEG", quality=quality, optimize=True)
            buffer.seek(0)
            return buffer.getvalue()
    except Exception as e:
        print(f"Error comprimiendo {image_path}: {e}")
        return None

def upload_dataset():
    print(f"--- SUBIDA OPTIMIZADA A FIREBASE (REDTRAIN) ---")
    print(f"Key: {KEY_PATH}")
    print(f"Bucket: {BUCKET_NAME}")
    
    if not os.path.exists(KEY_PATH):
        print(f"❌ ERROR: No encuentro la llave '{KEY_PATH}'")
        return

    # Init Firebase
    cred = credentials.Certificate(KEY_PATH)
    try:
        # Use a unique name for this app to avoid conflict with download_firebase app
        app = firebase_admin.initialize_app(cred, {
            'storageBucket': BUCKET_NAME
        }, name='uploader_app')
    except ValueError:
        app = firebase_admin.get_app('uploader_app')
        
    bucket = storage.bucket(app=app)
    
    print("\nComenzando escaneo y subida...")
    
    total_files = 0
    uploaded_files = 0
    skipped_files = 0
    errors = 0
    
    for root, dirs, files in os.walk(DATASET_ROOT):
        for file in files:
            if not file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.webp')):
                continue
                
            total_files += 1
            local_path = os.path.join(root, file)
            
            # Construct remote path
            # dataset/train/sculptures/foto.jpg -> dataset_v3_compressed/train/sculptures/foto.jpg
            rel_path = os.path.relpath(local_path, DATASET_ROOT)
            remote_path = f"{REMOTE_FOLDER}/{rel_path}".replace("\\", "/") # Enforce forward slashes
            
            blob = bucket.blob(remote_path)
            
            # Check if exists (Deduplication)
            if blob.exists():
                print(f"[{total_files}] SKIP (Ya existe): {remote_path}")
                skipped_files += 1
                continue
                
            # Compress
            compressed_data = compress_image(local_path)
            if not compressed_data:
                errors += 1
                continue
                
            # Upload
            try:
                print(f"[{total_files}] UPLOAD: {remote_path} ({len(compressed_data)/1024:.1f} KB)")
                blob.upload_from_string(compressed_data, content_type='image/jpeg')
                uploaded_files += 1
            except Exception as e:
                print(f"❌ Error subiendo {remote_path}: {e}")
                errors += 1

    print("\n" + "="*40)
    print(f"RESUMEN FINAL")
    print(f"Total escaneados: {total_files}")
    print(f"Subidos: {uploaded_files}")
    print(f"Saltados (Existen): {skipped_files}")
    print(f"Errores: {errors}")
    print("="*40)

    # --- UPLOAD MODEL .H5 (IF EXISTS) ---
    model_file = "model.h5"
    if os.path.exists(model_file):
        print(f"\nDetectado '{model_file}'. Subiendo a la raíz del bucket...")
        blob = bucket.blob(model_file)
        blob.upload_from_filename(model_file)
        print(f"✅ MODELO SUBIDO: {model_file}")
    else:
        print(f"\n(No se encontró '{model_file}', solo se subió el dataset)")

if __name__ == "__main__":
    upload_dataset()
