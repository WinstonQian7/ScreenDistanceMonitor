import json

#Uses Ivan Ludvig's eye distance algorithm to compute distance from screen 
class eyeDistance:
	DIS_BTW_EYES = 63 #average distance between eyes 63mm
	def __init__(self):
		#Load camera specifications and image Dimension from json
		fpath_cam = 'calibration_cam/json/camSpecs.json'
		fpath_img = 'calibration_cam/json/imgDimension.json'
		try:
			with open(fpath_cam, 'r') as json_file:
				self.spec = json.load(json_file)
		except OSError:
			print("Could not open/read file", fpath)
		try:
			with open(fpath_img, 'r') as json_file:
				self.imgDimension = json.load(json_file)
		except OSError:
			print("Could not open/read file", fpath)
	def eyePos(self,leftEyePos,rightEyePos):
		#calculates distance from screen using (x,y) of the center of both eyes
		deltaX_eye = abs(leftEyePos[0] - rightEyePos[0])
		deltaY_eye = abs(leftEyePos[1] - rightEyePos[1])

		if deltaX_eye >= deltaY_eye:
			distance = self.spec['focal_length'] * (self.DIS_BTW_EYES/self.spec['sensorSize'][0]) * (self.imgDimension['imageDimension'][0]/deltaX_eye)
		else:
			distance = self.spec['focal_length'] * (self.DIS_BTW_EYES/self.spec['sensorSize'][1]) * (self.imgDimension['imageDimension'][1]/deltaY_eye)

		distanceCM = distance/10 #Distance in cm
		distanceIN = distanceCM / 2.54 #Distance in In
		return (distanceCM,distanceIN)


