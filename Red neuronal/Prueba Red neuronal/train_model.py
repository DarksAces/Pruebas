import os
import tensorflow as tf

# Optimization: Use all available CPU cores for parallelism
num_threads = os.cpu_count()
tf.config.threading.set_inter_op_parallelism_threads(num_threads)
tf.config.threading.set_intra_op_parallelism_threads(num_threads)

from tensorflow.keras import layers, models, applications
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
import numpy as np
import json
import shutil
import multiprocessing

class ArtClassifier:
    def __init__(self, data_dir="dataset", model_path="best_model.h5", img_size=(224, 224), batch_size=32):
        self.data_dir = data_dir
        self.model_path = model_path
        self.img_size = img_size
        self.batch_size = batch_size
        self.history = None
        
    def load_data(self):
        # OPTIMIZATION: Mixed Precision for 11th Gen Intel (AVX512 users)
        try:
            from tensorflow.keras import mixed_precision
            # Check if we can use mixed precision (usually requires GPU, but good practice to set global policy)
            # For CPU only, often float32 is default, but we can stick to standard defaults to avoid "blowing up"
            pass 
        except:
            pass

        # Data augmentation
        train_datagen = ImageDataGenerator(
            rescale=1./255,
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True,
            fill_mode='nearest',
            validation_split=0.2
        )

        # Batch size 32 is safe for 16GB RAM. 
        # Using larger batches might consume too much RAM with large dataset.
        self.train_generator = train_datagen.flow_from_directory(
            self.data_dir,
            target_size=self.img_size,
            batch_size=self.batch_size,
            class_mode='categorical',
            subset='training'
        )

        self.validation_generator = train_datagen.flow_from_directory(
            self.data_dir,
            target_size=self.img_size,
            batch_size=self.batch_size,
            class_mode='categorical',
            subset='validation'
        )
        
        self.num_classes = self.train_generator.num_classes
        self.class_indices = self.train_generator.class_indices
        print(f"Classes found: {self.class_indices}")

    def build_model(self):
        # MobileNetV2 is efficient for CPU training (lightweight)
        self.base_model = applications.MobileNetV2(
            weights='imagenet',
            include_top=False,
            input_shape=(self.img_size[0], self.img_size[1], 3)
        )
        
        self.base_model.trainable = False

        model = models.Sequential([
            self.base_model,
            layers.GlobalAveragePooling2D(),
            layers.Dense(128, activation='relu'),
            layers.Dropout(0.5),
            layers.Dense(self.num_classes, activation='softmax')
        ])

        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        self.model = model
        return model

    def train(self, total_epochs=100):
        if not hasattr(self, 'train_generator'):
            self.load_data()
            
        # Callbacks common config
        checkpoint = tf.keras.callbacks.ModelCheckpoint(
            self.model_path, monitor='val_acc', save_best_only=True, mode='max', verbose=1
        )
        reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss', factor=0.2, patience=3, min_lr=1e-7, verbose=1
        )
        
        # --- PHASE 1: Feature Extraction (Training only the top layers) ---
        print("\n=== PHASE 1: Training Top Layers (Feature Extraction) ===")
        print("Freezing base model layers...")
        self.base_model.trainable = False
        self.model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        
        # Phase 1 typically needs fewer epochs to stabilize
        phase1_epochs = 20 
        early_stop_p1 = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
        
        self.model.fit(
            self.train_generator,
            epochs=phase1_epochs,
            validation_data=self.validation_generator,
            callbacks=[early_stop_p1, checkpoint],
            workers=os.cpu_count() - 2,
            use_multiprocessing=False 
        )
        
        # --- PHASE 2: Fine-Tuning (Training the whole network) ---
        print("\n=== PHASE 2: Fine-Tuning (Deep Training) ===")
        print("Unfreezing base model layers for fine adjustments...")
        self.base_model.trainable = True
        
        # Important: Needs a much lower learning rate to avoid destroying learned weights
        fine_tune_optimizer = tf.keras.optimizers.Adam(learning_rate=1e-5)
        
        self.model.compile(
            optimizer=fine_tune_optimizer,
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        # Phase 2 runs for the remaining time/epochs with high patience
        early_stop_p2 = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=15, restore_best_weights=True)
        
        self.history = self.model.fit(
            self.train_generator,
            epochs=total_epochs, # This continues from 0 in Keras count, but effectively it's a new run
            validation_data=self.validation_generator,
            callbacks=[early_stop_p2, checkpoint, reduce_lr],
            workers=os.cpu_count() - 2,
            use_multiprocessing=False 
        )
        
    def evaluate_and_save(self):
        # Model is already saved by Checkpoint, but we do a final eval
        val_loss, val_acc = self.model.evaluate(self.validation_generator)
        print(f"Final Validation Accuracy: {val_acc:.4f}")
        self.save_metadata(val_acc)
            
    def save_metadata(self, accuracy):
        metadata = {
            "accuracy": float(accuracy),
            "classes": self.class_indices,
            "architecture": "MobileNetV2_Transfer"
        }
        with open("model_metadata.json", "w") as f:
            json.dump(metadata, f, indent=4)

if __name__ == "__main__":
    # Ensure data exists
    if not os.path.exists("dataset"):
        print("Dataset directory not found! Run data_collector.py first.")
    else:
        classifier = ArtClassifier()
        classifier.load_data()
        classifier.build_model()
        classifier.train(total_epochs=50) # Increased epochs for better training
        classifier.evaluate_and_save()
