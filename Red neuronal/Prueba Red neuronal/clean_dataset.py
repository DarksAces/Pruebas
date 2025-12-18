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

    print(f"\nLimpieza completada. Se eliminaron {removed} archivos corruptos.")

def sync_classes(base_path="dataset"):
    print("\n--- SINCRONIZANDO CLASES (Train vs Validation) ---")
    train_dir = os.path.join(base_path, "train")
    val_dir = os.path.join(base_path, "validation")
    
    if not os.path.exists(train_dir) or not os.path.exists(val_dir):
        print("No se encontraron carpetas train/validation.")
        return

    # Obtener carpetas (clases)
    train_classes = set(os.listdir(train_dir))
    val_classes = set(os.listdir(val_dir))
    
    # Calcular diferencias
    only_in_train = train_classes - val_classes
    only_in_val = val_classes - train_classes
    
    # Borrar sobrantes en Train
    for cls in only_in_train:
        path = os.path.join(train_dir, cls)
        print(f"⚠️ Eliminando clase en TRAIN (no existe en validation): {cls}")
        try:
            # Recursive delete
            import shutil
            shutil.rmtree(path)
        except Exception as e:
            print(f"Error borrando {path}: {e}")

    # Borrar sobrantes en Validation
    for cls in only_in_val:
        path = os.path.join(val_dir, cls)
        print(f"⚠️ Eliminando clase en VALIDATION (no existe en train): {cls}")
        try:
            import shutil
            shutil.rmtree(path)
        except Exception as e:
            print(f"Error borrando {path}: {e}")
            
    if not only_in_train and not only_in_val:
        print("✅ Clases sincronizadas. Todo correcto.")

if __name__ == "__main__":
    sync_classes("dataset") # Ejecutar primero la sincronización
    clean_dataset("dataset")
