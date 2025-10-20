import os
import re
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

def sanitize_folder_name(name):
    # Eliminar letras y mantener solo números, puntos y comas
    name = re.sub(r'[a-zA-Z]', '', name)
    name = re.sub(r'(?<=\d)\.(?=\d)', ',', name)
    return re.sub(r'[^0-9.,]', '', name)

def rename_files_and_move_up(source_dir, dest_dir):
    if not os.path.isdir(source_dir):
        raise ValueError(f"El directorio fuente '{source_dir}' no existe o no es válido.")
    if not os.path.isdir(dest_dir):
        os.makedirs(dest_dir)

    for folder_name in os.listdir(source_dir):
        folder_path = os.path.join(source_dir, folder_name)
        if not os.path.isdir(folder_path):
            continue
        
        sanitized_name = sanitize_folder_name(folder_name)
        file_names = sorted(os.listdir(folder_path))
        
        for index, file_name in enumerate(file_names, 1):
            old_path = os.path.join(folder_path, file_name)
            if not os.path.isfile(old_path):
                continue
            new_file_name = f"{sanitized_name} {index}.jpg"
            target_path = os.path.join(folder_path, new_file_name)

            # Evitar sobrescrituras
            count = index
            while os.path.exists(target_path):
                count += 1
                new_file_name = f"{sanitized_name} {count}.jpg"
                target_path = os.path.join(folder_path, new_file_name)
            
            os.rename(old_path, target_path)

        # Mover archivos al directorio raíz
        for renamed_file in os.listdir(folder_path):
            src_file = os.path.join(folder_path, renamed_file)
            if os.path.isfile(src_file):
                shutil.move(src_file, os.path.join(source_dir, renamed_file))

        # Eliminar la carpeta vacía
        shutil.rmtree(folder_path)

    # Mover la carpeta raíz procesada al destino
    final_dest = os.path.join(dest_dir, os.path.basename(source_dir))
    if os.path.exists(final_dest):
        shutil.rmtree(final_dest)
    shutil.move(source_dir, dest_dir)

def main():
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal

    messagebox.showinfo("Selecciona", "Selecciona la carpeta con subcarpetas a procesar")
    source_directory = filedialog.askdirectory(title="Seleccionar directorio fuente")
    if not source_directory:
        messagebox.showerror("Cancelado", "No se seleccionó un directorio fuente.")
        return

    messagebox.showinfo("Selecciona", "Selecciona la carpeta de destino final")
    destination_directory = filedialog.askdirectory(title="Seleccionar directorio destino")
    if not destination_directory:
        messagebox.showerror("Cancelado", "No se seleccionó un directorio de destino.")
        return

    try:
        rename_files_and_move_up(source_directory, destination_directory)
        messagebox.showinfo("Éxito", "Las imágenes fueron procesadas correctamente.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    main()
