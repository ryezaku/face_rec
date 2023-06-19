
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
import tensorflow as tf
physical_devices = tf.config.list_physical_devices('GPU') 
tf.config.experimental.set_memory_growth(physical_devices[0], True)
import logging
from fastapi import FastAPI
import uvicorn
from typing import Optional
from FR.FaceRecognition.FaceRecognition import FaceRecognitionService
from FR import constant
from pydantic import BaseModel

class JsonInputFr(BaseModel):
	name: str
	frontIcImagePath:str
	selfiePhotoPath: str
	processImagePath:str
	faceSimilaritiesMinPercentage:Optional[float] = None

os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
path = os.path.dirname(os.path.abspath(__file__))
pathRecord = os.path.join(path, constant.LOG_FILENAME)
logging.basicConfig(level=logging.INFO, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s', datefmt='%Y-%m-%d %H:%M:%S', handlers=[logging.handlers.TimedRotatingFileHandler(pathRecord,'midnight',1)])

app = FastAPI()
faceRecognitionService = FaceRecognitionService()
@app.post('/face/recognition')
def faceImageRecognition(inputRequest:JsonInputFr):
	jsonInput = {}
	jsonInput['name'] = inputRequest.icNumber
	jsonInput['selfiePhotoPath1'] = inputRequest.frontIcImagePath
	jsonInput['selfiePhotoPath'] = inputRequest.selfiePhotoPath
	jsonInput['processImagePath'] = inputRequest.processImagePath
	if inputRequest.faceSimilaritiesMinPercentage is not None:
		jsonInput['faceSimilaritiesMinPercentage'] = inputRequest.faceSimilaritiesMinPercentage
	logging.info('Starting face recognition logging for ' + jsonInput['name'])
	croppedImagePath = {}
	faceRecognitionResponse = FaceRecognitionService.startFaceRecognition(jsonInput, faceRecognitionService,pathRecord, croppedImagePath)
	return faceRecognitionResponse


	uvicorn.run(app, host='127.0.0.1', port=5000, debug=True)
	
