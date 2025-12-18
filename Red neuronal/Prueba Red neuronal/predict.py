import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import sys
import os

def predict_image(image_path):
    if not os.path.exists('model.h5'):
        print("Error: No se encuentra el modelo 'model.h5'. Entrena el modelo primero.")
        return

    try:
        model = load_model('model.h5')
    except Exception as e:
        print(f"Error cargando el modelo: {e}")
        return

    # Mapeo de índices a etiquetas (debe coincidir con el entrenamiento)
    # Nota: El orden alfabético por defecto es artworks, monuments, others si no se especifica lo contrario
    # Es mejor verificar train_generator.class_indices después de entrenar
    class_names = ['artworks', 'monuments', 'others'] 

    try:
        img = image.load_img(image_path, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = x / 255.0

        predictions = model.predict(x)
        score = tf.nn.softmax(predictions[0])
        
        predicted_class_index = np.argmax(predictions[0])
        predicted_class = class_names[predicted_class_index]
        confidence = np.max(predictions[0])

        print(f"\nImagen: {image_path}")
        print(f"Predicción: {predicted_class}")
        print(f"Confianza: {confidence:.2%}")
        
    except Exception as e:
        print(f"Error procesando la imagen: {e}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python predict.py <ruta_de_la_imagen>")
    else:
        predict_image(sys.argv[1])
