import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tempfile import NamedTemporaryFile
from typing import Tuple
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "model/tf-cnn-model.h5") 
np.set_printoptions(suppress=True)

def predict_digit_file(file) -> Tuple[int, int]:
    # Save file to disk
    with NamedTemporaryFile(delete=False) as tmp:
        tmp.write(file.read())
        tmp_path = tmp.name

    # MATCH EXACT STEPS FROM try.py
    img = cv2.imread(tmp_path)
    img = cv2.resize(img, (640, 480))                         # STEP 1
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)          # STEP 2
    img_array = cv2.bitwise_not(img_gray)                     # STEP 3
    img_array = cv2.resize(img_array, (28, 28))               # STEP 4
    img_array = img_array.reshape((-1, 28, 28, 1))  /255.0          # STEP 5

    # Predict
    model = load_model(MODEL_PATH)
    prediction = model.predict(img_array)[0]
    number = int(np.argmax(prediction))
    confidence = int(prediction[number] * 100)

    return number, confidence
