
import cv2
import numpy as np
import tensorflow as tf
import time
import linecache
import sys
import logging
import logging.handlers  
import uuid
import psutil
tf.compat.v1.enable_eager_execution()
from retinaface import RetinaFace
from deepface import DeepFace

from PIL import ImageFile
from FR.commons import commons
from FR import constant
ImageFile.LOAD_TRUNCATED_IMAGES = True
class FaceRecognitionService:

	def __init__(self):
		
		self.modelArcFace = DeepFace.build_model('Facenet512')
		self.faceDetector = RetinaFace.build_model()

	def errorResponse(self,errorName):
		error = { "isAllKycIcProcessCompleted": False, "errorMessage": None, "facerecResult": {
    	"documentStatus": [errorName]}}
		return error

	def faceRecognition(self, selfiePhotoRgb, idCardRgb, faceSimilaritiesMinPercentage, inputIcNumber,jsonInput,croppedImagePath):
		isFaceRecProcessCompleted = True
		errorMessage = None
		facerecResult = None
		sameface = False
		similarityScore = 0
		selfieFace = RetinaFace.extract_faces(selfiePhotoRgb, align = True, model = self.faceDetector)
		idCardFace = RetinaFace.extract_faces(idCardRgb, align = True, model = self.faceDetector)
		if (len(selfieFace) == 1  and len(idCardFace) == 1):
			selfieFace = selfieFace[0]
			idCardFace = idCardFace[0]
			selfieFaceBgr = cv2.cvtColor(selfieFace, cv2.COLOR_RGB2BGR)
			idCardFaceBgr = cv2.cvtColor(idCardFace, cv2.COLOR_RGB2BGR)
			cv2.imwrite(jsonInput['processImagePath'] + constant.PATH_SEPARATOR + constant.CROPPED_SELFIE_FACE, selfieFaceBgr)
			croppedImagePath[constant.CROPPED_SELFIE_FACE_STRING]= constant.CROPPED_SELFIE_FACE
			cv2.imwrite(jsonInput['processImagePath'] + constant.PATH_SEPARATOR + constant.CROPPED_IDFACE_FACE_RECOGNITION, idCardFaceBgr)
			croppedImagePath[constant.CROPPED_IC_FACE_RECOGNITION_STRING] = constant.CROPPED_IDFACE_FACE_RECOGNITION 
			selfieFaceEmbeddings = commons.getFacialEmbeddings(selfieFace, self.modelArcFace)
			idCardFaceEmbeddings = commons.getFacialEmbeddings(idCardFace, self.modelArcFace)
			dist = commons.findCosineDistance(selfieFaceEmbeddings, idCardFaceEmbeddings)
			if (faceSimilaritiesMinPercentage ==0):
				faceSimilaritiesMinPercentage = 65.0
			similarityScore = round(1/(1+dist)*100,2)
			if (similarityScore >= faceSimilaritiesMinPercentage):
				sameface = True
			faceCondition = None


			facerecResult = {"sameFace":sameface, "similarityScore":similarityScore, "faceCondition":"GOOD"}
			frResult = {'errorMessage': errorMessage, 'facerecResult': facerecResult}
			return frResult
		elif(len(selfieFace)>1 or len(idCardFace)>1):
			isFaceRecProcessCompleted = False
			errorString ="Unexpected error occur upon kyc ic process with ic number "+ str(inputIcNumber) + ":" + "MULTIPLE_FACE_DETECTED"
			facerecResult = None
			frResult = {'isFaceRecProcessCompleted': isFaceRecProcessCompleted, 'errorMessage': errorString, 'facerecResult': facerecResult}
			return frResult
		elif(len(selfieFace)==0 or len(idCardFace)==0):
			isFaceRecProcessCompleted = False
			errorString = "Unexpected error occur upon kyc ic process with ic number "+ str(inputIcNumber) + ":" + "NO_FACE_DETECTED"
			facerecResult = None
			frResult = {'isFaceRecProcessCompleted': isFaceRecProcessCompleted, 'errorMessage': errorString, 'facerecResult': facerecResult}
			return frResult

	def faceRecognitionProcess(jsonInput, faceRecognitionService, croppedImagePath):
		start = time.time()
		makeDirectories = commons.makeDirectories(jsonInput)
		selfiePhotoPath = jsonInput['selfiePhotoPath']
		idCardPath = jsonInput['selfiePhotoPath1']
		inputIcNumber = jsonInput['icNumber']
		frontIcImage = cv2.imread(idCardPath)
		faceSimilaritiesMinPercentage = 0
		croppedImagePath[constant.CROPPED_FRONT_IC_FACE_RECOGNITION_NAME] = constant.CROPPED_IC_FACE_RECOGNITION
		if 'faceSimilaritiesMinPercentage' in jsonInput:
			faceSimilaritiesMinPercentage = jsonInput['faceSimilaritiesMinPercentage']
		selfiePhoto = cv2.imread(selfiePhotoPath)
		cv2.imwrite(jsonInput['processImagePath'] + constant.PATH_SEPARATOR + constant.SELFIE_IMAGE, selfiePhoto) 
		croppedImagePath[constant.SELFIE_IMAGE_STRING] = constant.SELFIE_IMAGE
		idCard = frontIcImage
		selfiePhotoRgb = cv2.cvtColor(selfiePhoto, cv2.COLOR_BGR2RGB)
		idCardRgb = cv2.cvtColor(idCard, cv2.COLOR_BGR2RGB)
		faceRecognitionResult = faceRecognitionService.faceRecognition(selfiePhotoRgb, idCardRgb, faceSimilaritiesMinPercentage,inputIcNumber, jsonInput, croppedImagePath)
		end = time.time()
		timeTaken = round(end - start,2)
		faceRecognitionResult["processTime"] = timeTaken
		return faceRecognitionResult
	
	def exceptionResponseFaceRecognition(jsonInput, ex, pathRecord):
		logging.basicConfig(filename=pathRecord, level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
		isFaceRecProcessCompleted = False
		trace = []
		tb = ex.__traceback__
		print(sys.exc_info())
		while tb is not None:
			linecache.checkcache(tb.tb_frame.f_code.co_filename)
			line = linecache.getline(tb.tb_frame.f_code.co_filename, tb.tb_lineno, tb.tb_frame.f_globals)
			trace.append({
				"filename": tb.tb_frame.f_code.co_filename,
				"method": tb.tb_frame.f_code.co_name,
				"line": tb.tb_lineno,
				"detail": line
			})	
			tb = tb.tb_next
		if 'icNumber' in jsonInput:			
			errorString = "Unexpected error occur upon face recognition process with ic number " + str(jsonInput['icNumber'])  
		else:
			errorString = "Unexpected error occur face recognition process " 
		facerecResult = None
		errorMessage = {"detail": errorString, "traceback":trace}
		exceptionResult = {'isFaceRecProcessCompleted': isFaceRecProcessCompleted, 'errorMessage': errorMessage, 'facerecResult': facerecResult, 'remarks': str(ex)}
		
		return exceptionResult

	def startFaceRecognition(jsonInput,faceRecognitionService, pathRecord,croppedImagePath):
		try: 
			frResult = FaceRecognitionService.faceRecognitionProcess(jsonInput, faceRecognitionService, croppedImagePath)
			return frResult
		except Exception as ex:
			exceptionResult = FaceRecognitionService.exceptionResponseFaceRecognition(jsonInput, ex, pathRecord)
			return exceptionResult