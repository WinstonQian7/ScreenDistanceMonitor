# import the necessary packages
from threading import Thread
import cv2
class WebcamVideoStream:
	def __init__(self, src=0,width=640,height=480):
		# initialize the video camera stream and read the first frame
		# from the stream
		self.stream = cv2.VideoCapture(src)
		(self.grabbed, self.frame) = self.stream.read()
		self.dimension = (width,height) 
		# initialize the variable used to indicate if the thread should
		# be stopped
		self.stopped = False
	def start(self):
		# start the thread to read frames from the video stream
		Thread(target=self.update, args=()).start()
		return self
	def update(self):
		# keep looping infinitely until the thread is stopped
		while True:
			# if the thread indicator variable is set, stop the thread
			if self.stopped:
				return
			# otherwise, read the next frame from the stream
			(self.grabbed, self.frame) = self.stream.read()
			self.frame = cv2.resize(self.frame,self.dimension,interpolation=cv2.INTER_AREA)
	def read(self):
		# return the frame most recently read
		return self.frame
	def stop(self):
		# indicate that the thread should be stopped
		self.stopped = True
	def resizeFrame(self):
		self.frame = cv2.resize(self.frame,self.dimension,interpolation=cv2.INTER_AREA)
		return self.frame
	def getFrameDimension(self):
		return self.dimension
	def emptyFrame(self):
		return True if self.grabbed == 0 else False
	def getCameraResolution(self):
		w = self.stream.get(cv2.CAP_PROP_FRAME_WIDTH)
		h = self.stream.get(cv2.CAP_PROP_FRAME_HEIGHT)
		return (w,h)

	
