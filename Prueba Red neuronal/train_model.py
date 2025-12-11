import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
import os

# Configuración
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 10
LEARNING_RATE = 0.0001
DATASET_DIR = 'dataset'

def train():
    # Rutas
    train_dir = os.path.join(DATASET_DIR, 'train')
    val_dir = os.path.join(DATASET_DIR, 'validation')

    # Verificar que existen los directorios
    if not os.path.exists(train_dir) or not os.path.exists(val_dir):
        print(f"Error: No se encuentra el directorio de datos en {DATASET_DIR}")
        print("Asegúrate de tener la estructura: dataset/train y dataset/validation")
        return

    # Generadores de datos con Data Augmentation para entrenamiento
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )

    val_datagen = ImageDataGenerator(rescale=1./255)

    print("Cargando datos...")
    train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical'
    )

    validation_generator = val_datagen.flow_from_directory(
        val_dir,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical'
    )

    # Transfer Learning con MobileNetV2
    base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=IMG_SIZE + (3,))
    
    # Congelar capas base
    base_model.trainable = False

    # Añadir capas personalizadas
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(1024, activation='relu')(x)
    # 3 clases: monuments, artworks, others
    predictions = Dense(3, activation='softmax')(x)

    model = Model(inputs=base_model.input, outputs=predictions)

    model.compile(optimizer=Adam(learning_rate=LEARNING_RATE),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    print("\nComenzando entrenamiento...")
    try:
        history = model.fit(
            train_generator,
            epochs=EPOCHS,
            validation_data=validation_generator
        )
        
        # Guardar el modelo
        model.save('model.h5')
        print("\nModelo guardado exitosamente como 'model.h5'")
        
        # Imprimir mapeo de clases
        print("\nMapeo de clases:")
        print(train_generator.class_indices)

    except Exception as e:
        print(f"\nError durante el entrenamiento: {e}")
        print("Posible causa: No hay suficientes imágenes en las carpetas.")

if __name__ == '__main__':
    train()
