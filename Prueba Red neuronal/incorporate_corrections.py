import os
import shutil
import sys

def incorporate_corrections():
    corrections_dir = 'predicted_results'
    dataset_dir = os.path.join('dataset', 'train')

    if not os.path.exists(corrections_dir):
        print(f"Error: La carpeta '{corrections_dir}' no existe.")
        return

    if not os.path.exists(dataset_dir):
        print(f"Error: La carpeta de dataset '{dataset_dir}' no existe.")
        return

    print("Iniciando incorporación de correcciones...")
    
    moved_count = 0
    
    # Recorrer cada subcarpeta en predicted_results (labels)
    for class_name in os.listdir(corrections_dir):
        class_path = os.path.join(corrections_dir, class_name)
        
        # Ignorar si no es una carpeta
        if not os.path.isdir(class_path):
            continue
            
        # Asegurarse de que la carpeta de destino exista en dataset/train
        target_class_path = os.path.join(dataset_dir, class_name)
        if not os.path.exists(target_class_path):
            print(f"Creando nueva categoría en dataset: {class_name}")
            os.makedirs(target_class_path)
            
        # Mover imágenes
        for filename in os.listdir(class_path):
            src_file = os.path.join(class_path, filename)
            
            # Solo procesar archivos
            if not os.path.isfile(src_file):
                continue
                
            dst_file = os.path.join(target_class_path, filename)
            
            # Manejar colisiones de nombres
            if os.path.exists(dst_file):
                base, ext = os.path.splitext(filename)
                counter = 1
                while os.path.exists(dst_file):
                    dst_file = os.path.join(target_class_path, f"{base}_corrected_{counter}{ext}")
                    counter += 1
            
            try:
                shutil.move(src_file, dst_file)
                moved_count += 1
                print(f"Movido: {filename} -> {class_name}")
            except Exception as e:
                print(f"Error moviendo {filename}: {e}")

    # Limpieza: eliminar carpetas vacías en predicted_results
    for class_name in os.listdir(corrections_dir):
        class_path = os.path.join(corrections_dir, class_name)
        if os.path.isdir(class_path) and not os.listdir(class_path):
            os.rmdir(class_path)

    print(f"\n¡Proceso completado! Se han incorporado {moved_count} imágenes al dataset.")
    print("Ahora puedes re-entrenar el modelo.")

if __name__ == '__main__':
    incorporate_corrections()
