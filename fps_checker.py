import datetime
class FPS:
	def __init__(self):
		# store the start time, end time, and total number of frames
		# that were examined between the start and end intervals
		self._start = None
		self._end = None
		self._numFrames = 0
		self._sleep_time = 0
	#@staticmethod
	def start(self):
		# start the timer
		self._start = datetime.datetime.now()
		return self
	#@staticmethod
	def stop(self):
		# stop the timer
		self._end = datetime.datetime.now()
	#@staticmethod
	def update(self):
		# increment the total number of frames examined during the
		# start and end intervals
		self._numFrames += 1
	#@staticmethod
	def elapsed(self):
		# return the total number of seconds between the start and
		# end interval
		return (self._end - self._start).total_seconds()
	#@staticmethod
	def fps(self):
		# compute the (approximate) frames per second
		non_sleep_time = self.elapsed() - self._sleep_time
		return self._numFrames / non_sleep_time
	def sleep_time(self, time):
		#subtracts time spend sleep
		self._sleep_time += time
