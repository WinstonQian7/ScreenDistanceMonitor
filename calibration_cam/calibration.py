import numpy as np
import cv2 as cv
import glob
import math
import json
import user_settings
"""
CALCULATIONS EXPLAINED

Calculate needed parameters for distance calculation (sensorSize and focal_length)
sensorSize or focal length must be known to complete calculation 
1. sensorSize is known and focal length is not known
    calibrateCam() -> calculateFocalLengthCV2(imgDimension['imageDimension'])
2. sensorSize is not known and focal length is known
    a) pixelSize is known
        calculateCamResolution() ->  calculateSensorSizePixelSize()
    b) DFOV is known, HFOV/VFOV is unknown
        (calculateHFOV()/calculateVFOV()) -> calculateSensoSize()

PARAMETERS USED

If sensorSize and focal_length is known, no need to run calibration script
camSpecs.json: DFOV,HFOV,VFOV,sensorSize,focal_length,pixelSize, camResolution
{   
    'DFOV': None, #diagnoal FOV
    'HFOV': None, #horizontal FOV
    'VFOV': None, #vertical FOV
    'sensorSize': None, #(w,h) in mm
    'focal_length': None, #F(mm) 
    'pixelSize': None, #(w,h) in µm NOT image resolution
    'camResolution': None #(w,h) in pixels
}
imgDimension.json: imageDimension
{
    'imageDimension': [400,400] #(w,h) in pixels
}
       
"""
class Calibration:
    def __init__(self,specifications):
        self.matrix = None
        self.spec = specifications
        self.spec['sensorSize'] = tuple(self.spec['sensorSize'])
        print(self.spec['sensorSize'])

    def calibrateCam(self):
        #Calibrate camera using chessboard
        # termination criteria
        criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        objp = np.zeros((6*7,3), np.float32)
        objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)
        # Arrays to store object points and image points from all the images.
        objpoints = [] # 3d point in real world space
        imgpoints = [] # 2d points in image plane.
        images = glob.glob('calibration_cam/calibration_images/*.jpg')
        for fname in images:
            img = cv.imread(fname)
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            # Find the chess board corners
            ret, corners = cv.findChessboardCorners(gray, (7,6), None)
            # If found, add object points, image points (after refining them)
            if ret == True:
                objpoints.append(objp)
                corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
                imgpoints.append(corners)
                # Draw and display the corners
                #cv.drawChessboardCorners(img, (7,6), corners2, ret)
                #cv.imshow('img', img)
                #cv.waitKey(500)
        cv.destroyAllWindows()
        ret, self.matrix, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    def calculateHFOV(self):
        try:
            self.spec['HFOV'] = 2 * math.atan(math.tan(self.spec['DFOV'])*math.cos(math.atan(self.spec['camResolution'][1]/self.spec['camResolution'][0])))
        except ZeroDivisionError:
            print("Cannot divide by Zero. Entered {}x{} valid webcam resolution.".format(self.spec['camResolution'][1],self.spec['camResolution'][0]))
    def calculateVFOV(self):
        try:
            self.spec['VFOV'] = 2 * math.atan(math.tan(self.spec['DFOV'])*math.sin(math.atan(self.spec['camResolution'][1]/self.spec['camResolution'][0])))
        except ZeroDivisionError:
            print("Cannot divide by Zero. Entered {}x{} valid webcam resolution.".format(self.spec['camResolution'][1],self.spec['camResolution'][0]))
    def calculateSensorSize(self):
        #SensorWidth(mm) = tan(toRadians(HFOV/2))*2*F(mm) (eq)
        sensorW = (float) (math.tan(math.toRadians(self.spec['HFOV']/2))*2*self.spec['focal_length'])
        sensorH = (float) (math.tan(math.toRadians(self.spec['VFOV']/2))*2*self.spec['focal_length'])
        self.spec['sensorSize'] = (sensorW,sensorH)
    def calculateFocalLengthCV2(self,imageDimension):
        #focal length in mm, sensorSize in mm
        self.spec['HFOV'],self.spec['VFOV'],self.spec['focal_length'],_,_ = cv.calibrationMatrixValues(self.matrix,imageDimension,self.spec['sensorSize'][0],self.spec['sensorSize'][1])
        return self.spec['focal_length']
    def calculateSensorSizePixelSize(self):
        #Only if pixelSize(wxh) is given in Camera specifications
        sensorW = self.spec['pixelSize'][0] * self.spec['camResolution'][0]
        sensorH = self.spec['pixelSize'][1] * self.spec['camResolution'][1]
        self.sensorSize = (sensorW,sensorH)
    def calculateCamResolution(self):
        if self.spec['camResolution'] == None:
            print(self.spec['camResolution'])
        else:
            cam = WebcamVideoStream(src=0,width=setImageSize[0],height=setImageSize[1])
            cam.start()
            print('[INFO] Capturing from webcam...')
            self.spec['camResolution'] = cam.getCameraResolution()
            cam.stop()
            fpath_cam = 'user_settings/camera_specifications/camSpecs.json'
        return self.spec['camResolution']
    def calibrationSuccess(self):
        if self.spec['focal_length'] == None or self.spec['sensorSize'] == None:
            print(self.spec['sensorSize'],self.spec['focal_length'])
            return False
        else:
            fpath_cam = 'user_settings/camera_specifications/camSpecs.json'
            try:
                with open(fpath_cam, 'w') as json_file:
                    json.dump(self.spec , json_file, indent=4)
            except OSError:
                print("Could not open/write file",fpath_cam)
            return True

def calibrate():
    fpath_cam = 'user_settings/camera_specifications/camSpecs.json'
    fpath_img = 'user_settings/camera_specifications/imgDimension.json'
    try:
        with open(fpath_cam, 'r') as json_file:
            spec = json.load(json_file)
    except OSError:
        print("Could not open/read file", fpath_cam)
    
    try:
        with open(fpath_img, 'r') as json_file:
            imgDimension = json.load(json_file)
    except OSError:
        print("Could not open/read file", fpath_img)
    setup = Calibration(spec)
    imgDimension['imageDimension'] = tuple(imgDimension['imageDimension'])
    if spec['focal_length'] != None and spec['sensorSize'] != None:
        pass 
    elif spec['sensorSize'] != None:
        setup.calibrateCam()
        spec['focal_length'] = setup.calculateFocalLengthCV2(imgDimension['imageDimension'])
        print('[INFO] calibration length: {:.3f}'.format(spec['focal_length']))
    elif spec['focal_length'] != None:
        if spec['pixelSize'] != None:
            spec['camResolution'] = setup.calculateCamResolution()
            spec['sensorSize'] = setup.calculateSensorSizePixelSize()
        elif spec['DFOV'] != None:
            if spec['HFOV'] == None:
                spec['HFOV'] = setup.calculateHFOV()
            elif spec['VFOV'] == None:
                spec['VFOV'] = setup.calculateVFOV()
            spec['sensorSize'] = setup.calculateSensorSize()
    #Checks if sensorSize and focal_length is defined
    if setup.calibrationSuccess() == False:
        raise TypeError('Required conditions for eye distance detection not satisfied.')
    else:
        print('Required conditions for eye distance detection have been meet')

calibrate()