import os
from PIL import Image

DATASET_DIR = "dataset"

def clean_images():
    print(f"Escaneando '{DATASET_DIR}' en busca de imágenes corruptas...")
    deleted_count = 0
    checked_count = 0

    for root, dirs, files in os.walk(DATASET_DIR):
        for file in files:
            filepath = os.path.join(root, file)
            checked_count += 1
            
            try:
                with Image.open(filepath) as img:
                    img.verify() # Verificar integridad
            except (IOError, SyntaxError) as e:
                print(f"[CORRUPTA] Eliminando: {filepath} - Error: {e}")
                os.remove(filepath)
                deleted_count += 1
            except Exception as e:
                print(f"[ERROR GENÉRICO] Eliminando: {filepath} - Error: {e}")
                os.remove(filepath)
                deleted_count += 1

    print(f"\nResumen: {checked_count} analizadas. {deleted_count} eliminadas.")

if __name__ == "__main__":
    clean_images()
