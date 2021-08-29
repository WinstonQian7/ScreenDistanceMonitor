import pytest
import gui
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QAction

@pytest.fixture
def app(qtbot):
	test_gui = gui.QWidget()
	qtbot.addWidget(test_gui)
	messagebox = QtWidgets.QApplication.activeWindow()
	exit_button = messagebox.button(QtWidgets.QMessageBox.Yes)
	qtbot.mouseClick(yes_button,QtCore.Qt.LeftButton,delay=1)
	return test_gui

@pytest.mark.great
def test_label(app):
    assert app.label.text() == "Notification cooldown period"

def test_label_2(app):
    assert app.label_2.text() == "Detection Status"

def test_label_3(app):
    assert app.label_3.text() == "Displayed distance"

def test_label_4(app):
    assert app.label_4.text() == "Step 1 - Click on start detection and grab a ruler"

def test_label_5(app):
    assert app.label_5.text() == "Enter Displayed Distance in Inches (option 1 only)"

def test_label_6(app):
    assert app.label_6.text() == "Step 2 -  Place the ruler on the computer webcam and measure a fixed distance, (ex: 12 inches) straight outward from the screen"

def test_label_7(app):
    assert app.label_7.text() == "Step 3 Move your face to the 12 inches mark and make sure a displayed distance is being detected (make sure displayed distance is consistent)"

def test_label_8(app):
    assert app.label_8.text() == "Step 4  - Stop Detection"

def test_label_9(app):
    assert app.label_9.text() == "Step 5 - Record the displayed distance and measured distance in the Enter Displayed/Measured Distance (calibration only) box (displayed distance may be different from measured distance) and click apply button"

def test_label_10(app):
    assert app.label_10.text() == "Settings"

def test_label_11(app):
    assert app.label_11.text() == "Camera Focal Length in mm"

def test_label_12(app):
    assert app.label_12.text() == "Camera sensor size in mm (width)"

def test_label_13(app):
    assert app.label_13.text() == "Camera sensor size in mm (height)"

def test_label_14(app):
    assert app.label_14.text() == "Instructions: Sensor size, width and height, need to be filled out. It is also acceptable to enter both focal length and sensor size information. *Please use option 1 if distance displayed isn\'t accurate"

def test_label_15(app):
    assert app.label_15.text() == "Enter Measured Distance in Inches (option 1 only)"

def test_label_16(app):
    assert app.label_16.text() == "Webcam selection (0 - default webcam, 1 - connected webcam, etc)"
