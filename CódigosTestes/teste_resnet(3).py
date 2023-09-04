# -*- coding: utf-8 -*-
"""Teste_Resnet(3).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1D1Dlina5IYM2Sw9niFjJikUqfE4BcJKl
"""

import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras.applications import ResNet50
from keras.layers import GlobalAveragePooling2D, Dense, BatchNormalization, Dropout
from keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import classification_report

from google.colab import drive
drive.mount('/content/drive')

train_dir = "/content/drive/MyDrive/Projeto_Pneumonia/chest_xray/train"
test_dir = "/content/drive/MyDrive/Projeto_Pneumonia/chest_xray/test"
val_dir = "/content/drive/MyDrive/Projeto_Pneumonia/chest_xray/val"

#Gerador de imagens pré-processamento
image_generator = ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.1,
    shear_range=0.1,
    zoom_range=0.1,
    samplewise_center=True,
    samplewise_std_normalization=True
)

#Gerador dados treinamento e validação
train_generator = image_generator.flow_from_directory(
    train_dir,
    batch_size=8,
    shuffle=True,
    class_mode='binary',
    target_size=(180, 180)
)

validation_generator = image_generator.flow_from_directory(
    val_dir,
    batch_size=1,
    shuffle=False,
    class_mode='binary',
    target_size=(180, 180)
)

#Resnet
resnet_base_model = ResNet50(
    input_shape=(180, 180, 3),
    include_top=False,
    weights='imagenet'
)

#Camadas personalizadas
resnet_model = tf.keras.Sequential([
    resnet_base_model,
    GlobalAveragePooling2D(),
    Dense(512, activation="relu"),
    BatchNormalization(),
    Dropout(0.6),
    Dense(128, activation="relu"),
    BatchNormalization(),
    Dropout(0.4),
    Dense(64, activation="relu"),
    BatchNormalization(),
    Dropout(0.3),
    Dense(1, activation="sigmoid")
])

#Compilando Resnet
opt = tf.keras.optimizers.Adam(learning_rate=0.001)
METRICS = [
    'accuracy',
    tf.keras.metrics.Precision(name='precision'),
    tf.keras.metrics.Recall(name='recall'),
]
resnet_model.compile(optimizer=opt, loss='binary_crossentropy', metrics=METRICS)

# Treinando modelo

# Calcular o peso das classes com base na contagem
num_normal = len(os.listdir(os.path.join(train_dir, 'NORMAL')))
num_pneumonia = len(os.listdir(os.path.join(train_dir, 'PNEUMONIA')))

weight_for_0 = num_pneumonia / (num_normal + num_pneumonia)
weight_for_1 = num_normal / (num_normal + num_pneumonia)

class_weight = {0: weight_for_0, 1: weight_for_1}

history = resnet_model.fit(
    train_generator,
    epochs=15,
    validation_data=validation_generator,
    class_weight=class_weight,
    steps_per_epoch=100,
    validation_steps=25
)

# Métricas para treinamento
train_metrics = resnet_model.evaluate(train_generator, steps=len(train_generator))
train_loss, train_accuracy, train_precision, train_recall = train_metrics

# Métricas para validação
val_metrics = resnet_model.evaluate(validation_generator, steps=len(validation_generator))
val_loss, val_accuracy, val_precision, val_recall = val_metrics

# Calcular F1 Score manualmente para treinamento
f1_train = 2 * (train_precision * train_recall) / (train_precision + train_recall)

# Calcular F1 Score manualmente para validação
f1_val = 2 * (val_precision * val_recall) / (val_precision + val_recall)

# Exibir métricas
print("Métricas de Treinamento:")
print(f"Loss: {train_loss:.4f}")
print(f"Acurácia: {train_accuracy * 100:.2f}%")
print(f"Precisão: {train_precision * 100:.2f}%")
print(f"Recall: {train_recall * 100:.2f}%")
print(f"F1 Score (Treinamento): {f1_train * 100:.2f}%")

print("\nMétricas de Validação:")
print(f"Loss: {val_loss:.4f}")
print(f"Acurácia: {val_accuracy * 100:.2f}%")
print(f"Precisão: {val_precision * 100:.2f}%")
print(f"Recall: {val_recall * 100:.2f}%")
print(f"F1 Score (Validação): {f1_val * 100:.2f}%")