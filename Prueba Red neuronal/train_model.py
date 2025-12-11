import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
import os

# Configuración
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 10
DATASET_DIR = 'dataset/train'
VALIDATION_DIR = 'dataset/validation'
MODEL_FILE = 'model.h5'

def train_network():
    # Detectar número de clases dinámicamente
    if not os.path.exists(DATASET_DIR):
        print(f"❌ Error: No existe la carpeta {DATASET_DIR}")
        return

    classes = [d for d in os.listdir(DATASET_DIR) if os.path.isdir(os.path.join(DATASET_DIR, d))]
    num_classes = len(classes)
    print(f"✅ Se han detectado {num_classes} categorías: {classes}")

    if num_classes < 2:
        print("❌ Error: Necesitas al menos 2 categorías para entrenar.")
        return

    # Generadores de datos (Data Augmentation)
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
        DATASET_DIR,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical'
    )

    validation_generator = val_datagen.flow_from_directory(
        VALIDATION_DIR,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical'
    )

    # Modelo Base (MobileNetV2)
    base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    
    # Congelar modelo base
    base_model.trainable = False

    # Capas personalizadas
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(1024, activation='relu')(x)
    x = Dropout(0.2)(x)
    # Capa de salida dinámica según número de clases encontradas
    predictions = Dense(num_classes, activation='softmax')(x)

    model = Model(inputs=base_model.inputs, outputs=predictions)

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    print("\nComenzando entrenamiento...")
    history = model.fit(
        train_generator,
        epochs=EPOCHS,
        validation_data=validation_generator
    )

    # Guardar modelo
    model.save(MODEL_FILE)
    print(f"\nModelo guardado exitosamente como '{MODEL_FILE}'")
    
    # Guardar mapeo de clases para referencia
    print("\nMapeo de clases:")
    print(train_generator.class_indices)

if __name__ == "__main__":
    train_network()
