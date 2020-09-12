import tensorflow as tf
import matplotlib.pyplot as plt 
import numpy as np 
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os
import pdb
import math

VALIDATION_SPLIT = 0.2
base_dir = "D:gobot"
train_dir = os.path.join(base_dir, "train")

train_map = os.path.join(train_dir, "map")
train_catch = os.path.join(train_dir, "catch")
train_caught = os.path.join(train_dir, "pokemon_caught")
train_pokestop = os.path.join(train_dir, "pokestop")

num_train_map = len(os.listdir(train_map)) 
num_train_catch = len(os.listdir(train_catch))
num_train_caught = len(os.listdir(train_caught))
num_train_pokestop = len(os.listdir(train_pokestop))

num_validation_map = math.floor(num_train_map * VALIDATION_SPLIT)
num_validation_catch = math.floor(num_train_catch * VALIDATION_SPLIT)
num_validation_caught = math.floor(num_train_caught * VALIDATION_SPLIT)
num_validation_pokestop = math.floor(num_train_pokestop * VALIDATION_SPLIT)

num_train_map -= num_validation_map
num_train_catch -= num_validation_catch
num_train_caught -= num_validation_caught
num_train_pokestop -= num_validation_pokestop


total_train = num_train_map + num_train_catch + num_train_caught + num_train_pokestop
total_validation = num_validation_map + num_validation_catch + num_validation_caught + num_validation_pokestop

BATCH_SIZE = 32
IMG_SHAPE = 150

train_image_generator = ImageDataGenerator(
    rescale = 1./255,
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode = 'nearest',
    validation_split=VALIDATION_SPLIT

)
validation_image_generator = ImageDataGenerator(rescale = 1./255)

train_data_gen = train_image_generator.flow_from_directory(batch_size=BATCH_SIZE, directory=train_dir, shuffle=True, target_size=(IMG_SHAPE, IMG_SHAPE), subset='training')
val_data_gen = validation_image_generator.flow_from_directory(batch_size=BATCH_SIZE, directory=train_dir, shuffle=True, target_size=(IMG_SHAPE, IMG_SHAPE), subset='validation')

model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=[IMG_SHAPE, IMG_SHAPE, 3]),
    tf.keras.layers.MaxPooling2D(2, 2),

    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'), 
    tf.keras.layers.MaxPooling2D(2, 2),

    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'), 
    tf.keras.layers.MaxPooling2D(2, 2),

    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'), 
    tf.keras.layers.MaxPooling2D(2, 2),

    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(256, activation="relu"),
    tf.keras.layers.Dense(4, activation="softmax")
])

model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=['accuracy'])

model.summary()

EPOCHS = 5

history = model.fit(
    train_data_gen, 
    steps_per_epoch= total_train//BATCH_SIZE,
    epochs = EPOCHS,
    validation_data = val_data_gen,
    validation_steps = total_validation//BATCH_SIZE
)

model.save("./models/gameStateModel.h5")

# analysis
acc = history.history["accuracy"]
val_acc = history.history["val_accuracy"]

loss = history.history["loss"]
val_loss = history.history["val_loss"]

epochs_range = range(EPOCHS)

plt.figure(figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label="Training Accuracy")
plt.plot(epochs_range, val_acc, label="Validation Accuracy")
plt.legend(loc="lower right")
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label="Training Loss")
plt.plot(epochs_range, val_loss, label="Validation Loss")
plt.legend(loc="upper right")
plt.title('Training and Validation Loss')
plt.show()
