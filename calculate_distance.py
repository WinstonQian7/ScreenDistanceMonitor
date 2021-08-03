import json

#Uses Ivan Ludvig's eye distance algorithm to compute distance from screen 
class EyeDistance:
	DIS_BTW_EYES = 63 #average distance between eyes 63mm
	def __init__():
		#Load camera specifications and image Dimension from json
		EyeDistance.loadJSON()
	@staticmethod
	def loadJSON():
		fpath_cam = 'calibration_cam/json/camSpecs.json'
		fpath_img = 'calibration_cam/json/imgDimension.json'
		try:
			with open(fpath_cam, 'r') as json_file:
				spec = json.load(json_file)
		except OSError:
			print("Could not open/read file", fpath)
		try:
			with open(fpath_img, 'r') as json_file:
				imgDimension = json.load(json_file)
		except OSError:
			print("Could not open/read file", fpath)
		return (spec,imgDimension)
	@staticmethod
	def eyePos(leftEyePos,rightEyePos):
		#calculates distance from screen using (x,y) of the center of both eyes
		spec,imgDimension = EyeDistance.loadJSON()
		deltaX_eye = abs(leftEyePos[0] - rightEyePos[0])
		deltaY_eye = abs(leftEyePos[1] - rightEyePos[1])

		if deltaX_eye >= deltaY_eye:
			distance = spec['focal_length'] * (EyeDistance.DIS_BTW_EYES/spec['sensorSize'][0]) * (imgDimension['imageDimension'][0]/deltaX_eye)
		else:
			distance = spec['focal_length'] * (EyeDistance.DIS_BTW_EYES/spec['sensorSize'][1]) * (imgDimension['imageDimension'][1]/deltaY_eye)

		distanceCM = distance/10 #Distance in cm
		distanceIN = distanceCM / 2.54 #Distance in In
		return [distanceCM,distanceIN]


