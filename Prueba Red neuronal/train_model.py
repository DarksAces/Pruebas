import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
import os

# Configuración
IMG_SIZE = (224, 224)
# Configuración
IMG_SIZE = (224, 224)
BATCH_SIZE = 64 # AUMENTADO: Procesa el doble de fotos por segundo
EPOCHS = 500 # Fase 1: Calentamiento (GOD MODE)
DATASET_DIR = 'dataset/train'
VALIDATION_DIR = 'dataset/validation'
MODEL_FILE = 'model.h5'

def train_network():
    # Generadores de datos
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

    validation_datagen = ImageDataGenerator(rescale=1./255)

    print("Cargando imágenes...")
    train_generator = train_datagen.flow_from_directory(
        DATASET_DIR,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical'
    )

    validation_generator = validation_datagen.flow_from_directory(
        VALIDATION_DIR,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical'
    )

    # Crear modelo base pre-entrenado
    base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=IMG_SIZE + (3,))
    
    # Congelar capas base inicialmente
    base_model.trainable = False

    # Añadir capas personalizadas
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(1024, activation='relu')(x)
    x = Dropout(0.5)(x)
    predictions = Dense(train_generator.num_classes, activation='softmax')(x)

    model = Model(inputs=base_model.input, outputs=predictions)

    # Compilar modelo (Fase 1: Adam)
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])


    # Callbacks para "Modo Avanzado" - ULTRA RESISTENCIA
    callbacks = [
        # EarlyStopping desactivado para que entrene SÍ o SÍ hasta el final
        # EarlyStopping(monitor='val_accuracy', patience=50, verbose=1, restore_best_weights=True),
        ModelCheckpoint(MODEL_FILE, monitor='val_accuracy', save_best_only=True, verbose=1)
    ]

    print("\nComenzando entrenamiento AVANZADO (Fase 1: Calentamiento)...")
    history = model.fit(
        train_generator,
        epochs=EPOCHS,
        validation_data=validation_generator,
        callbacks=callbacks,

    )

    # --- FASE 2: FINE-TUNING (Adam) ---
    print("\n>>> INICIANDO FASE 2: FINE-TUNING (Refinamiento con Adam) <<<")
    
    # Descongelar el modelo base para ajustar pesos profundos
    base_model.trainable = True
    
    # Recompilar con Learning Rate MUY BAJO (1e-5)
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    FINE_TUNE_EPOCHS_ADAM = 300 
    total_epochs_phase2 = EPOCHS + FINE_TUNE_EPOCHS_ADAM

    print(f"Entrenando por {FINE_TUNE_EPOCHS_ADAM} épocas extra con ajuste fino (Adam)...")
    
    history_fine_adam = model.fit(
        train_generator,
        epochs=total_epochs_phase2,
        initial_epoch=history.epoch[-1] + 1,
        validation_data=validation_generator,
        callbacks=callbacks,

    )

    # --- FASE 3: POLISHING (SGD) ---
    print("\n>>> INICIANDO FASE 3: PULIDO FINAL (SGD) <<<")
    
    # Cambiamos a SGD (Stochastic Gradient Descent) con un LR minúsculo
    # El SGD suele encontrar mínimos más estables al final del entrenamiento
    model.compile(optimizer=tf.keras.optimizers.SGD(learning_rate=1e-5, momentum=0.9),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    FINE_TUNE_EPOCHS_SGD = 200
    total_epochs_phase3 = total_epochs_phase2 + FINE_TUNE_EPOCHS_SGD

    print(f"Entrenando por {FINE_TUNE_EPOCHS_SGD} épocas extra con SGD para pulido final...")

    history_fine_sgd = model.fit(
        train_generator,
        epochs=total_epochs_phase3,
        initial_epoch=history_fine_adam.epoch[-1] + 1,
        validation_data=validation_generator,
        callbacks=callbacks,

    )

    # Guardar modelo
    # Guardar modelo final (aunque el Checkpoint ya guardó el mejor)
    # model.save(MODEL_FILE) 
    print(f"\nEntrenamiento finalizado. El mejor modelo se guardó en '{MODEL_FILE}'")
    
    # Guardar mapeo de clases para referencia
    print("\nMapeo de clases:")
    print(train_generator.class_indices)

if __name__ == "__main__":
    train_network()
