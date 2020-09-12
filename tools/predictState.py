import tensorflow as tf
import cv2
import numpy as np
import pdb
import time

model = tf.keras.models.load_model("./tools/models/gameStateModel.h5")
def stateName(state):
    if 1. in state.tolist():
        x = state.tolist().index(1.)
    else:
        return None
    states = {
        0: "pokestop",
        1: "map", 
        2: "pokemon_caught", 
        3: "catch"
    }
    return states[x]

def predict(img):
    """
    PARAMETERS
    img: BGR cv2 image
    """
    img = cv2.resize(img, (150, 150))
    prediction = model.predict(np.array([img]))[0]
    return stateName(prediction)
