import os
import shutil
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array

# Configuración
MODEL_PATH = 'model.h5'
DATASET_DIR = 'dataset/train'
REVIEW_DIR = 'dataset_review'  # Carpeta donde moveremos las dudosas
CONFIDENCE_THRESHOLD = 0.70    # BAJAMOS UMBRAL: Si sospecha al 70%, que nos avise.

CLASSES = ['artworks', 'monuments', 'others']

def redistribute_dataset():
    print("Cargando modelo...")
    try:
        model = tf.keras.models.load_model(MODEL_PATH)
    except:
        print("❌ No se encontró el modelo. Entrena primero.")
        return

    if not os.path.exists(REVIEW_DIR):
        os.makedirs(REVIEW_DIR)

    print(f"--- INICIANDO AUDITORÍA DEL DATASET (MODO SENSIBLE) ---")
    print(f"Buscando imágenes sospechosas con >{CONFIDENCE_THRESHOLD*100}% de confianza.\n")

    moves_count = 0

    for current_label in CLASSES:
        folder_path = os.path.join(DATASET_DIR, current_label)
        if not os.path.exists(folder_path):
            continue
        
        print(f"Analizando carpeta: {current_label} ...")
        files = os.listdir(folder_path)
        total_files = len(files)
        
        for i, file in enumerate(files):
            if i % 100 == 0: print(f"  Procesando {i}/{total_files}...") # Feedback de progreso
            
            if not file.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.bmp')):
                continue
                
            file_path = os.path.join(folder_path, file)
            
            try:
                # Preprocesar imagen
                img = load_img(file_path, target_size=(224, 224))
                img_array = img_to_array(img)
                img_array = np.expand_dims(img_array, axis=0)
                img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)
                
                # Predecir
                predictions = model.predict(img_array, verbose=0)
                score = tf.nn.softmax(predictions[0])
                
                predicted_index = np.argmax(score)
                predicted_label = CLASSES[predicted_index]
                confidence = np.max(score)

                # Si el modelo cree que es otra cosa con >70% de seguridad
                if predicted_label != current_label and confidence > CONFIDENCE_THRESHOLD:
                    print(f"⚠️ DUDOSA: {file} está en '{current_label}' pero parece '{predicted_label}' ({confidence*100:.1f}%)")
                    
                    # Mover a carpeta de revisión
                    # Estructura: dataset_review/artworks_to_monuments/archivo.jpg
                    
                    move_folder = os.path.join(REVIEW_DIR, f"from_{current_label}_to_{predicted_label}")
                    if not os.path.exists(move_folder):
                        os.makedirs(move_folder)
                        
                    shutil.move(file_path, os.path.join(move_folder, file))
                    moves_count += 1
                    
            except Exception as e:
                print(f"Error analizando {file}: {e}")

    print(f"\n✅ Auditoría terminada. Se han movido {moves_count} imágenes a '{REVIEW_DIR}' para tu revisión.")

if __name__ == "__main__":
    redistribute_dataset()
