import os
import glob
from PIL import Image

def clean_dataset(folder_path):
    print(f"Limpiando dataset en: {folder_path}")
    image_files = glob.glob(os.path.join(folder_path, '**', '*'), recursive=True)
    
    count = 0
    removed = 0
    
    for file_path in image_files:
        if os.path.isdir(file_path):
            continue
            
        try:
            with Image.open(file_path) as img:
                img.verify() # Validar estructura interna de la imagen
        except (IOError, SyntaxError) as e:
            print(f"Eliminando archivo corrupto: {file_path}")
            try:
                os.remove(file_path)
                removed += 1
            except Exception as e:
                print(f"Error borrando {file_path}: {e}")
        
        count += 1
        if count % 1000 == 0:
            print(f"Procesadas {count} archivos...")

    print(f"\nLimpieza completada. Se eliminaron {removed} archivos corruptos.")

if __name__ == "__main__":
    clean_dataset("dataset")
