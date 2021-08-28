# Eye Distance Monitor for Desktops
Utlilizes OpenCV Computer Vision and adapts [Ivan Ludvig](https://ivanludvig.github.io/blog/2019/07/20/calculating-screen-to-face-distance-android
) research paper to detect if distance from webcam to computer screen is healthy (>24 inches). User will recieve windows toast notification if distance detected is consistantly less than threshold (<24 inches). Comes with two configuration methods (*Choose one*),
1. One time configuration - Measure distance from webcam to user using a ruler. Record the measured distance and displayed distance shown in the application (*Displayed distance will vary from measured distance during configuration)*. It is recommended to use a ruler pointing straight outward from your webcam to your eye level. 
2. Requires sensor size of the webcam you are currently using. *Varies from webcam manufacturer*

Currently supports Windows only, created by Winston Qian

#### Table of Contents <hr>
**[Project Usage](#usage)** <br>
**[Project Explained](#creation)** <br>
**[Why isn't my distance being detected?](#tips)** <br>
**[Future Improvements](#improve)** <br>
**[Author Notes](#notes)** <br>
**[Resources](#resources)** <br> <hr>

## <a name = "usage"></a> Project Usage:
```
pip install -r requirements.txt
```
Contains two files to run application:
  1. main.py - For developers to run CLI, see main.py for commands
  2. gui.py - To run PyQt GUI for application

**GUI Screenshots during detection**<br>
![gui_start_page](https://user-images.githubusercontent.com/37454624/131199285-398c069b-bb2e-4761-a3c5-8382fe582bc9.PNG)
![gui_ex_1](https://user-images.githubusercontent.com/37454624/131199259-a5e835d6-4cf2-4036-b920-57ac094f4ce4.PNG)
![gui_ex_2](https://user-images.githubusercontent.com/37454624/131199279-d8483503-6474-401d-b36d-2dbc074fa0bb.PNG)
![gui_ex_3](https://user-images.githubusercontent.com/37454624/131199282-1c056c86-970c-4216-9f21-f34da17b2678.PNG)
<br>**Notification Popup**<br>
![image](https://user-images.githubusercontent.com/37454624/131199173-49aa4a6a-5a31-4d37-91fa-78d370afb077.png)

## <a name = "creation"></a> Project Explained:
![formula](https://user-images.githubusercontent.com/37454624/131199726-019be45d-4dc1-42e5-bbc3-bbc236bb8230.PNG)
Credit to [Ivan Ludvig](https://ivanludvig.github.io/blog/2019/07/20/calculating-screen-to-face-distance-android for formula <br>

Project solves for variables in the formula, see [Ivan Ludvig](https://ivanludvig.github.io/blog/2019/07/20/calculating-screen-to-face-distance-android blog for more info. Utlilizes tensorflow dnn + haarcascades eyeglass model to obtain object height/width (location of center of eye relative to image). Images are preprocessed using OpenCV blobFromImage with a confidence level of 0.5 in order to use with tensorflow dnn to detect the face. Once the face is detected, the image is cropped so only the eye region is in the image. Image is then grayscaled and run with haarcascades eyeglass model. If two eyes are detected, the location of the eyes is passed to a function which calculates the distance from screen given the parameters. 

Detection is run every 60 frames in order to reduce the CPU demand for image processing, *Note my current computer isn't very good, feel free to change the detection rate*. In the period of 6 consecutive detections, if two or more detections were less than thereshold (<24 inches), windows notification is triggered. Once notification is triggered, the cooldown period will be displayed on the GUI and notifications will not be displayed during the cooldown period. 

## <a name="tips"></a> Why isn't my distance being detected?:
1. Check brightness of image, use camera app to check, too much brightness or darkness may distort the image
2. Check angle of camera, make sure your face is being captured by the webcam
3. Keeping your head and eyes pointed straight at the screen may improve detection rate
4. If wearing glasses, taking off your glasses may improve detection rate

## <a name="improve"></a> Future Improvements:
Eye detection for glasses could be improved (use better detection algorithm than haarcascades eyeglasses) <br>
Package into desktop application (exe) <br>
Enable usage on MacOS <br>

## <a name="notes"></a> Author Notes:
Project was inspired by my school design project which explored the usage of capacitors to detect eye distance from screen. After spending long amounts of time on the computer with bad habits, I decided to create the eye distance from screen application using webcams in place of sensors. I intended to create an application that is easy to use and not heavily cpu intensive so that all users can run the program. I originally wanted to have sensor size information as the only configuration method. However, webcam manufacturer often don't post the specifications needed so a manuel configuration was needed, *see calibration.py for functions implementing different formulas to obtain focal length and sensor size if interested*. I also explored different models to use, I wasn't able to find a model that was consistent at detecting eyes through glasses without consuming all of my cpu. As a result, I used haarcascades eyeglasses which can be inconsistent with detecting eyes through glasses at times.

## <a name="resources"></a> Resources
https://www.ni.com/en-us/support/documentation/supplemental/18/calculating-camera-sensor-resolution-and-lens-focal-length.html#:~:text=Sensor%20size%20refers%20to%20the%20physical%20size%20of,on%20the%20sensor%20and%20multiply%20by%20the%20resolution.

https://learnopencv.com/approximate-focal-length-for-webcams-and-cell-phone-cameras/#disqus_thread

https://ivanludvig.github.io/blog/2019/07/20/calculating-screen-to-face-distance-android

https://byteiota.com/face-recognition/

https://en.wikipedia.org/wiki/Image_sensor_format

https://medium.com/@stepanfilonov/tracking-your-eyes-with-python-3952e66194a6

https://towardsdatascience.com/real-time-eye-tracking-using-opencv-and-dlib-b504ca724ac6

https://www.toptenreviews.com/1080p-2-0-mega-pixels-understanding-webcam-technical-terms

https://www.pyimagesearch.com/2017/11/06/deep-learning-opencvs-blobfromimage-works/

