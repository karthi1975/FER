#!/usr/bin/env python3
"""
Dataset Integration for FER Project
Integrates with Kaggle FER dataset and provides training/evaluation capabilities
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import cv2
from fer_core import FEREngine

class FERDatasetIntegration:
    """
    Integration with FER datasets for training and evaluation
    """
    
    def __init__(self, dataset_path=None):
        self.dataset_path = dataset_path
        self.fer_engine = FEREngine()
        self.emotion_mapping = self.fer_engine.emotion_mapping
        
        # Reverse mapping for dataset labels
        self.reverse_mapping = {v: k for k, v in self.emotion_mapping.items()}
        
        # Supported emotions in our system
        self.supported_emotions = list(self.emotion_mapping.values())
        
    def load_kaggle_fer_dataset(self, data_dir):
        """
        Load Kaggle FER dataset
        Expected structure:
        data_dir/
        ├── train/
        │   ├── angry/
        │   ├── disgust/
        │   ├── fear/
        │   ├── happy/
        │   ├── sad/
        │   ├── surprise/
        │   └── neutral/
        └── test/
            └── (same structure)
        """
        print("📁 Loading Kaggle FER dataset...")
        
        train_data = []
        train_labels = []
        test_data = []
        test_labels = []
        
        # Load training data
        train_dir = os.path.join(data_dir, 'train')
        if os.path.exists(train_dir):
            for emotion in os.listdir(train_dir):
                emotion_path = os.path.join(train_dir, emotion)
                if os.path.isdir(emotion_path):
                    # Map emotion to our system
                    mapped_emotion = self.emotion_mapping.get(emotion, emotion)
                    
                    for img_file in os.listdir(emotion_path):
                        if img_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                            img_path = os.path.join(emotion_path, img_file)
                            try:
                                # Load and preprocess image
                                img = cv2.imread(img_path)
                                if img is not None:
                                    img = cv2.resize(img, (48, 48))  # Standard FER size
                                    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                                    img = img / 255.0  # Normalize
                                    
                                    train_data.append(img)
                                    train_labels.append(mapped_emotion)
                            except Exception as e:
                                print(f"Error loading {img_path}: {e}")
        
        # Load test data
        test_dir = os.path.join(data_dir, 'test')
        if os.path.exists(test_dir):
            for emotion in os.listdir(test_dir):
                emotion_path = os.path.join(test_dir, emotion)
                if os.path.isdir(emotion_path):
                    mapped_emotion = self.emotion_mapping.get(emotion, emotion)
                    
                    for img_file in os.listdir(emotion_path):
                        if img_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                            img_path = os.path.join(emotion_path, img_file)
                            try:
                                img = cv2.imread(img_path)
                                if img is not None:
                                    img = cv2.resize(img, (48, 48))
                                    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                                    img = img / 255.0
                                    
                                    test_data.append(img)
                                    test_labels.append(mapped_emotion)
                            except Exception as e:
                                print(f"Error loading {img_path}: {e}")
        
        # Convert to numpy arrays
        train_data = np.array(train_data)
        train_labels = np.array(train_labels)
        test_data = np.array(test_data)
        test_labels = np.array(test_labels)
        
        print(f"✅ Dataset loaded successfully!")
        print(f"   Training samples: {len(train_data)}")
        print(f"   Test samples: {len(test_data)}")
        print(f"   Supported emotions: {self.supported_emotions}")
        
        return train_data, train_labels, test_data, test_labels
    
    def create_fer_model(self, input_shape=(48, 48, 1), num_classes=7):
        """
        Create a CNN model for FER
        """
        model = keras.Sequential([
            # Input layer
            layers.Input(shape=input_shape),
            
            # First convolutional block
            layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25),
            
            # Second convolutional block
            layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25),
            
            # Third convolutional block
            layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25),
            
            # Flatten and dense layers
            layers.Flatten(),
            layers.Dense(512, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.5),
            layers.Dense(256, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.5),
            layers.Dense(num_classes, activation='softmax')
        ])
        
        return model
    
    def train_model(self, train_data, train_labels, test_data, test_labels, 
                   epochs=50, batch_size=32):
        """
        Train the FER model
        """
        print("🚀 Starting model training...")
        
        # Prepare data
        X_train = train_data.reshape(-1, 48, 48, 1)
        X_test = test_data.reshape(-1, 48, 48, 1)
        
        # Convert labels to categorical
        from sklearn.preprocessing import LabelEncoder
        le = LabelEncoder()
        y_train = le.fit_transform(train_labels)
        y_test = le.transform(test_labels)
        
        y_train = keras.utils.to_categorical(y_train, num_classes=7)
        y_test = keras.utils.to_categorical(y_test, num_classes=7)
        
        # Create and compile model
        model = self.create_fer_model()
        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        # Print model summary
        model.summary()
        
        # Callbacks
        callbacks = [
            keras.callbacks.EarlyStopping(patience=10, restore_best_weights=True),
            keras.callbacks.ReduceLROnPlateau(factor=0.5, patience=5),
            keras.callbacks.ModelCheckpoint('best_fer_model.h5', save_best_only=True)
        ]
        
        # Train model
        history = model.fit(
            X_train, y_train,
            validation_data=(X_test, y_test),
            epochs=epochs,
            batch_size=batch_size,
            callbacks=callbacks,
            verbose=1
        )
        
        # Evaluate model
        test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
        print(f"✅ Training completed!")
        print(f"   Test accuracy: {test_accuracy:.4f}")
        print(f"   Test loss: {test_loss:.4f}")
        
        return model, history, le
    
    def evaluate_model(self, model, test_data, test_labels, label_encoder):
        """
        Evaluate the trained model
        """
        print("📊 Evaluating model performance...")
        
        X_test = test_data.reshape(-1, 48, 48, 1)
        y_test = label_encoder.transform(test_labels)
        
        # Make predictions
        predictions = model.predict(X_test)
        predicted_labels = np.argmax(predictions, axis=1)
        
        # Generate classification report
        print("\n📈 Classification Report:")
        print(classification_report(y_test, predicted_labels, 
                                 target_names=label_encoder.classes_))
        
        # Generate confusion matrix
        cm = confusion_matrix(y_test, predicted_labels)
        
        # Plot confusion matrix
        plt.figure(figsize=(10, 8))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                   xticklabels=label_encoder.classes_,
                   yticklabels=label_encoder.classes_)
        plt.title('Confusion Matrix')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.tight_layout()
        plt.savefig('confusion_matrix.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return predictions, predicted_labels
    
    def plot_training_history(self, history):
        """
        Plot training history
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
        
        # Plot accuracy
        ax1.plot(history.history['accuracy'], label='Training Accuracy')
        ax1.plot(history.history['val_accuracy'], label='Validation Accuracy')
        ax1.set_title('Model Accuracy')
        ax1.set_xlabel('Epoch')
        ax1.set_ylabel('Accuracy')
        ax1.legend()
        ax1.grid(True)
        
        # Plot loss
        ax2.plot(history.history['loss'], label='Training Loss')
        ax2.plot(history.history['val_loss'], label='Validation Loss')
        ax2.set_title('Model Loss')
        ax2.set_xlabel('Epoch')
        ax2.set_ylabel('Loss')
        ax2.legend()
        ax2.grid(True)
        
        plt.tight_layout()
        plt.savefig('training_history.png', dpi=300, bbox_inches='tight')
        plt.show()

def main():
    """Main function to demonstrate dataset integration"""
    print("🎭 FER Dataset Integration Demo")
    print("=" * 50)
    
    # Initialize dataset integration
    fer_dataset = FERDatasetIntegration()
    
    # Example usage (uncomment when you have the dataset)
    """
    # Load dataset
    data_dir = "path/to/your/fer_dataset"
    train_data, train_labels, test_data, test_labels = fer_dataset.load_kaggle_fer_dataset(data_dir)
    
    # Train model
    model, history, label_encoder = fer_dataset.train_model(
        train_data, train_labels, test_data, test_labels
    )
    
    # Evaluate model
    predictions, predicted_labels = fer_dataset.evaluate_model(
        model, test_data, test_labels, label_encoder
    )
    
    # Plot training history
    fer_dataset.plot_training_history(history)
    """
    
    print("📚 Dataset integration ready!")
    print("💡 To use with your dataset:")
    print("   1. Download the FER dataset from Kaggle")
    print("   2. Extract to a folder")
    print("   3. Update the data_dir path in main()")
    print("   4. Uncomment the training code")
    print("   5. Run the script!")

if __name__ == "__main__":
    main()
