import numpy as np
import cv2 as cv
import glob
import math
import json


class calibration:
    def __init__(self,specifications):
        """
            If sensorSize and focal_length is known, no need to run calibration script
            DFOV,HFOV,VFOV,sensorSize,focal_length,pixelSize, camResolution
            spec =  {   
                        'DFOV': None, #diagnoal FOV
                        'HFOV': None, #horizontal FOV
                        'VFOV': None, #vertical FOV
                        'sensorSize': None, #(w,h) in mm
                        'focal_length': None, #F(mm) 
                        'pixelSize': None, #(w,h) in µm
                        'camResolution': None #(w,h) in pixels
                    }
        """
        self.matrix = None
        self.spec = specifications
    def calibrateCam(self):
        # termination criteria
        criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        objp = np.zeros((6*7,3), np.float32)
        objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)
        # Arrays to store object points and image points from all the images.
        objpoints = [] # 3d point in real world space
        imgpoints = [] # 2d points in image plane.
        images = glob.glob('*.jpg')
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
    def calculateSensorSizePixelSize(self):
        #Only if pixelSize(wxh) is given in Camera specifications
        sensorW = self.spec['pixelSize'][0] * self.spec['camResolution'][0]
        sensorH = self.spec['pixelSize'][1] * self.spec['camResolution'][1]
        self.sensorSize = (sensorW,sensorH)
    def calibrationSuccess(self):
        if self.spec['focal_length'] == None or self.spec['sensorSize'] == None:
            return False
        else:
            try:
                with open(fpath_cam, 'w') as json_file:
                    json.dump(spec , json_file, indent=4)
            except OSError:
                print("Could not open/write file",fpath_cam)
            return True

def main():
    fpath_cam = 'json/camSpecs.json'
    fpath_img = 'json/imgDimension.json'
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
    #SEE IF POSSIBLE TO IMPORT WEBCAMVIDEOSTREAM
    setup = calibration(spec)
    if spec['focal_length'] != None and spec['sensorSize'] != None:
        pass 
    elif spec['sensorSize'] != None:
        setup.calibrateCam()
        spec['focal_length'] = setup.calculateFocalLengthCV2(imgDimension['imageDimension'])
    elif spec['focal_length'] != None:
        if spec['pixelSize'] != None:
            spec['sensorSize'] = setup.calculateSensorSizePixelSize()
        elif spec['DFOV'] != None:
            if spec['HFOV'] == None:
                spec['HFOV'] = setup.calculateHFOV()
            elif spec['VFOV'] == None:
                spec['VFOV'] = setup.calculateVFOV()
            spec['sensorSize'] = setup.calculateSensorSize()
    
    
    if setup.calibrationSuccess() == False:
        raise TypeError('Required conditions for eye distance detection not satisfied.')
    else:
        print("Required conditions for eye distance detection have been meet")


      




if __name__ == "__main__":
    main()
    """
    spec =  {   
                'DFOV': None, #diagnoal FOV
                'HFOV': None, #horizontal FOV
                'VFOV': None, #vertical FOV
                'sensorSize': (), #(w,h) in mm
                'focal_length': None, #F(mm) or F(pixels) NEED TO MODIFY EVENTUALLY
                'pixelSize': None #(w,h) in µm 
            }
    c = calibration(spec)

    c.calibrateCam()
    """