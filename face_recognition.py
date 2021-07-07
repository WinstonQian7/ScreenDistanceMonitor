
import os
import cv2
import argparse
import numpy as np 
import time

#local modules
from win10toast import ToastNotifier
from calculate_distance import eyeDistance 
from WebcamVideoStream import WebcamVideoStream
from FPSCheck import FPS

class FaceDetection:
    net = None
    image_size = 160
    distance  = eyeDistance()
    eye_detect = None
    def __init__(self):
        FaceDetection.load_models()

    @staticmethod
    def load_models():
        if not FaceDetection.net:
            FaceDetection.net = FaceDetection.load_opencv()
        if not FaceDetection.eye_detect:
            FaceDetection.eye_detect = FaceDetection.load_haarcascade()

    @staticmethod
    def load_opencv():
        model_path = "./Models/OpenCV/opencv_face_detector_uint8.pb"
        model_pbtxt = "./Models/OpenCV/opencv_face_detector.pbtxt"
        net = cv2.dnn.readNetFromTensorflow(model_path, model_pbtxt)
        return net

    @staticmethod
    def load_haarcascade():
        model_path = 'models/OpenCV/haarcascade_eye_tree_eyeglasses.xml'
        classifier = cv2.CascadeClassifier(model_path)
        return classifier

    @staticmethod
    def detect_faces(image, display_images=False): # Make display_image to True to manually debug if you run into errors
        height, width, channels = image.shape

        blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300), [104, 117, 123], False, False)
        FaceDetection.net.setInput(blob)
        detections = FaceDetection.net.forward()

        faces = []

        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5:
                x1 = int(detections[0, 0, i, 3] * width)
                y1 = int(detections[0, 0, i, 4] * height)
                x2 = int(detections[0, 0, i, 5] * width)
                y2 = int(detections[0, 0, i, 6] * height)
                faces.append([x1, y1, x2 - x1, y2 - y1])

                if display_images:
                    cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 3)
    
        if display_images:
            print("Face co-ordinates: ", faces)
            cv2.imshow("Training Face", cv2.resize(image, (300, 300)))
            cv2.waitKey(0)
        return faces

    @staticmethod
    def fetch_detections(image, display_image_with_detections=False):
        
        faces = FaceDetection.detect_faces(image)
        #predictor = dlib.shape_predictor("Models/FaceDetection/shape_predictor_68_face_landmarks.dat")

        #detections = []
        if len(faces) == 1:
            x, y, w, h = faces[0]
            #im_face = image[y:y + h, x:x + w]
            #img = cv2.resize(im_face, (200, 200))
            im_face = image[int(y+h/4):int(y + h/2), x:x + w]
                    #im_face = image[int(y+h/4):int(y + h/2), x:int(x + w/2)]
                    #im_face = cv2.resize(im_face,(300,300))

            gray = cv2.cvtColor(im_face, cv2.COLOR_BGR2GRAY)
                    #im_face = cv2.resize(gray,(300,300))
                    #im_eye = image[int(y+h/4):int(y + h/2), x:int(x + w/2)]
                    #im_eye = cv2.resize(im_eye,(300,300))
                    #cv2.imshow("Detected", gray)
                    # Detect landmarks on "image_gray"
                  
                    #shape = FaceDetection.predictor(im_face, dlib.rectangle(x,y,(x+w),(y+h)))
                    #shape = face_utils.shape_to_np(shape)
                    # loop over the (x, y)-coordinates for the facial landmarks
                    # and draw them on the image
                    #for (x, y) in shape:
                    #cv2.circle(im_face, (x, y), 1, (0, 0, 255), -1)
            eyes = FaceDetection.eye_detect.detectMultiScale(gray, 1.05, 3)
            print(len(eyes))
            if len(eyes) == 2:
                leftEyePos = ()
                rightEyePos = ()
                faceHalf = w / 2
                for (x_eye,y_eye,w_eye,h_eye) in eyes:
                    cv2.rectangle(im_face, (x_eye,y_eye), (x_eye+w_eye, y_eye+h_eye), (0,0,255), 3)
                    getX = x_eye + w_eye/2
                    getY = y_eye + h_eye/2
                    if getX < faceHalf:
                        leftEyePos = (getX,getY)
                    else:
                        rightEyePos = (getX,getY)
                if leftEyePos != () and rightEyePos != ():
                    dis = FaceDetection.distance.eyePos(leftEyePos,rightEyePos) #(cm,in)
                    print("{:.1f} cm".format(dis[0]))
                    print("{:.1f} in".format(dis[1]))
                    cv2.imshow("Detected", cv2.resize(im_face,(300,300)))

                    if dis[1] < 24:
                        return 1 #eye distance is too close
                    elif dis[1] > 24 and dis[1] < 36:
                        return -1 #eye distance is ideal
                return 0 #eyes were not detected

                    #shape = predictor(im_face, dlib.rectangle(x, y, x+w, x+h))
                    #shape = face_utils.shape_to_np(shape)
                    #print("[INFO]:", (x,y),(x+w,y+h))
                    #for (x, y) in shape:
                    #    cv2.circle(im_face, (x, y), 1, (0, 0, 255), -1)
                    #cv2.putText(image, detected[0], (x, y - 4), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)


        #if display_image_with_detections and im_face != None: #additional check if face is found 
        #   cv2.imshow("Detected", im_face)

        #return detections

def face_recognition(display_image=False):
    FaceDetection.load_models()
    toaster = ToastNotifier()
    detected_count = 0
    fetched_count = 0
    sleep_time = 5
    setImageSize = (400,400) #can change in future
    cam = WebcamVideoStream(src=0,width=setImageSize[0],height=setImageSize[1])
    cam.start()
    sleep(2.0)
    print('[INFO] Capturing from webcam...')
    fps = FPS().start()
    while 1:
        image = cam.read()
        

        if cam.emptyFrame():
            print('[INFO] Finished detection')
            break
        if fps._numFrames % 60 == 0:
            eyedetection_status = FaceDetection.fetch_detections(image, True) 
            fetched_count += 1
            if eyedetection_status == 1: #eye distance is too close
                detected_count += 1
            elif eyedetection_status == -1: #eye distance is ideal
                detected_count = 0



        if fetched_count == 6:
            if detected_count >= 2:
                toaster.show_toast(
                        "Eyedistance Monitor",
                        "Too close to screen!", icon_path=None,
                        duration=5,threaded=False)
                time.sleep(sleep_time)
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


   