import cv2 
import qimage2ndarray
import sys 
import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication,QWidget,QLabel,QPushButton, \
	QVBoxLayout, QMainWindow
from PyQt5.QtMultimediaWidgets import QVideoWidget


class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.title = 'Distance Monitor GUI Interface'
		self.setWindowTitle(self.title)
		self.screen_size = QSize(600,600)
		self.initUI()

	def initUI(self):
		self.central_widget = QWidget()

		self.label = QLabel('No Camera Feed',self.central_widget)
		self.label.setFixedSize(self.screen_size)

		self.button_start = QPushButton('Start',self.central_widget)
		self.button_end = QPushButton('Exit', self.central_widget)
		
		self.button_start.clicked.connect(self.captureFrame)
		self.button_end.clicked.connect(sys.exit) 

		self.layout = QVBoxLayout(self.central_widget)
		self.layout.addWidget(self.button_start)
		self.layout.addWidget(self.button_end)
		self.layout.addWidget(self.label)
		self.setCentralWidget(self.central_widget)

	def captureFrame(self):
		self.cap = cv2.VideoCapture(0)
		self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.screen_size.width())
		self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.screen_size.height())

		self.timer = QTimer()
		self.timer.timeout.connect(self.displayFrame)
		self.timer.start(60)

	def displayFrame(self):
		ret, frame = self.cap.read()
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		image = QImage(frame, frame.shape[1], frame.shape[0], 
					   frame.strides[0], QImage.Format_RGB888)
		self.label.setPixmap(QPixmap.fromImage(image))

if __name__ == '__main__':
	app = QApplication([])
	window = MainWindow()
	window.show()
	app.exec_()



