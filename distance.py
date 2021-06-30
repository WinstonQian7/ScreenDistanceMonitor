
"""
class eyeDistance:
	def __init__(self):
		self.sensorSize = ()
		self.focal_length = 0
		self.img_dimension = getFrameDimension()
		self.rightEyePos = () #updated from project.py
		self.leftEyePos = () #updated from project.py
		self.pixelSize = ()
	def calculateSensorSize(self):
		sensorWidth = pixelSize[0] * img_dimension[0] 
		sensorHeight = pixelSize[1] * img_dimension[1]
		self.sensorSize = (sensorWidth, sensorHeight)
	def getSensorSize(self):
		return self.sensorSize
"""
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
	def eyePos(leftEyePos,rightEyePos):
		#leftEyePos = (290,67)
		#rightEyePos = (167.5,58.5)
		#445.5-330.5,68.5-79.5
		#359-227 94-72  
		#319-178 47-44  31.81 CM
		#290.0 - 167.5 67-58.5 36.62 CM
		deltaX_eye = abs(leftEyePos[0] - rightEyePos[0])
		deltaY_eye = abs(leftEyePos[1] - rightEyePos[1])

		if deltaX_eye >= deltaY_eye:
			distance = self.spec['focal_length'] * (self.DIS_BTW_EYES/self.spec['sensor'][0]) * (self.imgDimension['imageDimension'][0]/deltaX_eye)
		else:
			distance = self.spec['focal_length'] * (self.DIS_BTW_EYES/self.spec['sensor'][1]) * (self.imgDimension['imageDimension'][1]/deltaY_eye)

		distanceCM = distance/10 #Distance in cm
		distanceIN = distanceCM / 2.54
		print("{:.1f} cm".format(distanceCM))
		print("{:.1f} in".format(distanceIN))
		return (distanceCM,distanceIN)


