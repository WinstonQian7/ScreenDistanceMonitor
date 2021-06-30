# import libraries
import cv2
import argparse
import datetime
import time
from distance import eyeDistance #fix distance.py
from WebcamVideoStream import WebcamVideoStream
from FPSCheck import FPS
from threading import Thread, Timer
from win10toast import ToastNotifier


#ap = argparse.ArgumentParser()
#ap.add_argument(-d, --display, type=int, default=-1,
#    help='Whether or not frames should be displayed')
#args = vars(ap.parse_args())

# Load trained cascade classifier
CascadePath = {'eye': 'models/haarcascade_eye_tree_eyeglasses.xml',
                'face': 'models/haarcascade_frontalface_default.xml'}
eye_detect = cv2.CascadeClassifier(CascadePath['eye'])
face_detect = cv2.CascadeClassifier(CascadePath['face'])

# start camera / read video
setImageSize = (500,500) #can change in future
distance_obj = eyeDistance()
cam = WebcamVideoStream(src=0,width=setImageSize[0],height=setImageSize[1])
cam.start()
fps = FPS().start()
#frame_dimension = cam.getFrameDimension()

startTime = datetime.datetime.now()

def detectFace(frame):
    face = face_detect.detectMultiScale(frame, 1.3, 7)
    if len(face) == 1:
        for (x,y,w,h) in face:
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,255), 3)
        return 1
    return -1

def detectEyes(frame):
    # Convert color image into grayscale
    # Detect faces ROI
    #Syntax: Classifier.detectMultiScale(input image, Scale Factor , Min Neighbors)
    eyes = eye_detect.detectMultiScale(frame, 1.05, 6)
    
    # Draw rectangle around the faces
    if len(eyes) == 2:
        count = 0
        for (x,y,w,h) in eyes:
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,255), 3)
            getX = x + w/2
            getY = y + h/2
            if count == 0:
                leftEyePos = (getX,getY)
            else:
                rightEyePos = (getX,getY)
                return eyePos(leftEyePos,rightEyePos) #fix
            count += 1

while (datetime.datetime.now() - startTime).total_seconds()<= 10:
    # read frame from camera
    #cam.resizeFrame()
    frame = cam.read()

    # no frame then break loop
    if cam.emptyFrame():
        break
    #update every 60 frames
    if fps._numFrames % 120 == 0:
        gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        """
        face = face_detect.detectMultiScale(frame, 1.3, 7, minSize = (50,50))
        if len(face) == 1:
            for (x,y,w,h) in face:
                cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,255), 3)
            cv2.imshow('Live Eye Detection', frame) 
        """
        
        distance_from_cam = detectEyes(gray_img) #(cm,in) can use cm instead of in
        if distance_from_cam[2] <= 24:
            toaster = ToastNotifier()
            toaster.show_toast(
                "Eyedistance Monitor",
                "Too close to screen!", icon_path=None,
                duration=10,threaded=False)
            # Wait for threaded notification to finish
            while toaster.notification_active(): time.sleep(0.1)
        elif distance_from_cam < 24:
            pass
        cv2.putText(frame, distance_from_cam, (5, 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 0), 2)
        capturedFrame = frame
        cv2.imshow('Live Eye Detection', capturedFrame) 
        
    #wait to close window
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    fps.update()

fps.stop()

print('[INFO] elasped time: {:.2f}'.format(fps.elapsed()))
print('[INFO] approx. FPS: {:.2f}'.format(fps.fps()))

#cleanup 
cam.stop()
cv2.destroyAllWindows()