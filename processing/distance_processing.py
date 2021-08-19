
import os
import cv2
import argparse
import numpy as np 
import time

#local modules
import processing
from win10toast import ToastNotifier
from processing.calculate_distance import EyeDistance
from processing.WebcamVideoStream import WebcamVideoStream
from processing.fps_checker import FPS

class ScreenDistance:
    def __init__(self):
        self.net = None
        self.eye_detect = None
        self.load_models() #loads opencv dnn/haarcascades models

    def load_models(self):
        if not self.net:
            self.net = self.load_opencv()
        if not self.eye_detect:
            self.eye_detect = self.load_haarcascade()

    def load_opencv(self):
        model_path = "./Models/OpenCV/opencv_face_detector_uint8.pb"
        model_pbtxt = "./Models/OpenCV/opencv_face_detector.pbtxt"
        self.net = cv2.dnn.readNetFromTensorflow(model_path, model_pbtxt)
        return self.net

    def load_haarcascade(self):
        model_path = 'models/OpenCV/haarcascade_eye_tree_eyeglasses.xml'
        classifier = cv2.CascadeClassifier(model_path)
        return classifier

    def detect_faces(self,image): 
        height, width, channels = image.shape

        blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300), [104, 117, 123], False, False)
        self.net.setInput(blob)
        detections = self.net.forward()

        faces = []

        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5:
                x1 = int(detections[0, 0, i, 3] * width)
                y1 = int(detections[0, 0, i, 4] * height)
                x2 = int(detections[0, 0, i, 5] * width)
                y2 = int(detections[0, 0, i, 6] * height)
                faces.append([x1, y1, x2 - x1, y2 - y1])

        return faces

    def detect_eyes(self,image, display_image=False, info=False, adj_factor = 0):
        faces = self.detect_faces(image)
        if len(faces) == 1:
            x, y, w, h = faces[0]
            im_face = image[int(y+h/4):int(y + h/2), x:x + w]
                    #im_face = image[int(y+h/4):int(y + h/2), x:int(x + w/2)]
                    #im_face = cv2.resize(im_face,(300,300))
            gray = cv2.cvtColor(im_face, cv2.COLOR_BGR2GRAY) #converts to grayscale for eye detection
                    #im_face = cv2.resize(gray,(300,300))
                    #im_eye = image[int(y+h/4):int(y + h/2), x:int(x + w/2)]
                    #im_eye = cv2.resize(im_eye,(300,300))
                    #cv2.imshow("Detected", gray)
                    # Detect landmarks on "image_gray"
                  
                    #shape = ScreenDistance.predictor(im_face, dlib.rectangle(x,y,(x+w),(y+h)))
                    #shape = face_utils.shape_to_np(shape)
                    # loop over the (x, y)-coordinates for the facial landmarks
                    # and draw them on the image
                    #for (x, y) in shape:
                    #cv2.circle(im_face, (x, y), 1, (0, 0, 255), -1)
            eyes = self.eye_detect.detectMultiScale(gray, 1.05, 3)            
            if len(eyes) == 2:
                leftEyePos = []
                rightEyePos = []
                faceHalf = w / 2
                for (x_eye,y_eye,w_eye,h_eye) in eyes:
                    cv2.rectangle(im_face, (x_eye,y_eye), (x_eye+w_eye, y_eye+h_eye), (0,0,255), 3)
                    getX = x_eye + w_eye/2
                    getY = y_eye + h_eye/2
                    if getX < faceHalf:
                        leftEyePos = [getX,getY]
                    else:
                        rightEyePos = [getX,getY]
                if leftEyePos != [] and rightEyePos != []:
                    dis_obj = EyeDistance()
                    dis = dis_obj.eyePos(leftEyePos,rightEyePos) #(cm,in)
                    if adj_factor != 0: #Need to fix in interface
                        dis[1] += adj_factor
                    
                    if display_image:
                        cv2.imshow("Detected", cv2.resize(image[y:y+h,x:x+w], (300,240)))
                    if info:
                        if len(eyes) == 0:
                            print('[INFO] No Eyes are being detected')
                        else:
                            print('[INFO] {} eyes are being detected'.format(len(eyes)))
                            if dis != None:
                                print('[INFO] {:.1f} cm'.format(dis[0]))
                                print('[INFO] {:.1f} in'.format(dis[1]))
                    if dis[1] < 24:
                        return 1 #eye distance is too close
                    elif dis[1] > 24 and dis[1] < 36:
                        return -1 #eye distance is ideal
                return 0 #eyes were not detected

def runDetection(display_image=False, sleep_time=5, seconds_or_minutes=False, info=False, adj_factor=0):
    screen_distance = ScreenDistance() 
    screen_distance.load_models()
    toaster = ToastNotifier()
    detected_count = 0
    if seconds_or_minutes == False:
        sleep_time = sleep_time * 60
    else:
        sleep_time = sleep_time
    fetched_count = 0
    setImageSize = (400,400) #can change in future
    cam = WebcamVideoStream(src=0,width=setImageSize[0],height=setImageSize[1])
    cam.start()
    time.sleep(2.0)
    print('[STATUS] Capturing from webcam...')
    fps = FPS().start()
    while 1:
        image = cam.read()
        if cam.emptyFrame():
            print('[STATUS] Finished detection')
            break
        if fps._numFrames % 60 == 0: #Runs detection every 60 frames
            eyedetection_status = screen_distance.detect_eyes(image, display_image,info,adj_factor) 
            fetched_count += 1
            if eyedetection_status == 1: #eye distance is too close
                detected_count += 1
            elif eyedetection_status == -1: #eye distance is ideal
                detected_count = 0
        #6 detections if detections are either too close or eyes weren't found
        #If detections are far enough distance then fetched_count is reset to zero in previous code block
        #If two or more of the 6 detections were too close, windows notification is triggered for duration 
        #of sleep parameter
        if fetched_count == 6:
            if detected_count >= 2:
                toaster.show_toast(
                        "ScreenDistance Monitor",
                        "Too close to screen!", icon_path=None,
                        duration=sleep_time,threaded=False)
            fps.sleep_time(sleep_time)
            fetched_count = 0
            detected_count = 0
        key = cv2.waitKey(1)
        if key & 0xFF == ord("q"):
            break
        fps.update()

    fps.stop()

    print('[INFO] elasped time: {:.2f}'.format(fps.elapsed()))
    print('[INFO] approx. FPS: {:.2f}'.format(fps.fps()))

    #clean-up
    cam.stop()
    cv2.destroyAllWindows()


   