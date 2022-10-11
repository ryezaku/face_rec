import numpy as np
import os
import cv2
from deepface.commons import functions
from tensorflow.keras.preprocessing import image

def makeDirectories(jsonInput):
		if not os.path.exists(jsonInput['processImagePath']):
			os.makedirs(jsonInput['processImagePath'])
		return jsonInput['processImagePath']
def getFacialEmbeddings(img, model):
    inputShapeX, inputShapeY= functions.find_input_shape(model)
    img = cv2.resize(img, (inputShapeY,inputShapeX))
    imgPixels = image.img_to_array(img)
    imgPixels = np.expand_dims(imgPixels, axis = 0)
    imgPixels /= 255
    embedding = model.predict(imgPixels)[0].tolist()
    return embedding

def findCosineDistance(source_representation, test_representation):
    a = np.matmul(np.transpose(source_representation), test_representation)
    b = np.sum(np.multiply(source_representation, source_representation))
    c = np.sum(np.multiply(test_representation, test_representation))
    return 1 - (a / (np.sqrt(b) * np.sqrt(c)))

