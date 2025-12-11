import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import sys
import os
import glob

def predict_folder(folder_path):
    if not os.path.exists('model.h5'):
        print("Error: No se encuentra el modelo 'model.h5'. Entrena el modelo primero.")
        return

    if not os.path.exists(folder_path):
        print(f"Error: La carpeta '{folder_path}' no existe.")
        return

    try:
        model = load_model('model.h5')
    except Exception as e:
        print(f"Error cargando el modelo: {e}")
        return

    class_names = [
        'architecture', 'artworks', 'ceramics', 'drawings', 'frescoes', 
        'graffiti', 'monuments', 'mosaics', 'others', 'paintings', 
        'photography', 'sculptures', 'textiles'
    ]
    
    # Extensiones de imagen comunes
    extensions = ['*.jpg', '*.jpeg', '*.png', '*.webp', '*.JPG', '*.JPEG', '*.PNG']
    image_files = []
    
    for ext in extensions:
        image_files.extend(glob.glob(os.path.join(folder_path, ext)))

    if not image_files:
        print(f"No se encontraron imágenes en {folder_path}")
        return

    print(f"\nAnalizando {len(image_files)} imágenes en '{folder_path}'...\n")
    print(f"{'ARCHIVO':<40} | {'PREDICCIÓN':<15} | {'CONFIANZA'}")
    print("-" * 70)

    stats = {name: 0 for name in class_names}

    for img_path in image_files:
        try:
            img = image.load_img(img_path, target_size=(224, 224))
            x = image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            x = x / 255.0

            predictions = model.predict(x, verbose=0)
            predicted_class_index = np.argmax(predictions[0])
            predicted_class = class_names[predicted_class_index]
            confidence = np.max(predictions[0])
            
            stats[predicted_class] += 1
            
            filename = os.path.basename(img_path)
            # Acortar nombre si es muy largo para que quepa en la tabla
            if len(filename) > 35:
                filename = filename[:32] + "..."
                
            print(f"{filename:<40} | {predicted_class:<15} | {confidence:.2%}")

        except Exception as e:
            print(f"Error en {os.path.basename(img_path)}: {e}")

    print("-" * 70)
    print("\nRESUMEN:")
    for name, count in stats.items():
        if count > 0:
            print(f"{name.capitalize()}: {count}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python predict_folder.py <ruta_de_la_carpeta>")
    else:
        predict_folder(sys.argv[1])
