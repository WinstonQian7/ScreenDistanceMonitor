# Eye Distance Monitor for Desktops
Utlilizes OpenCV Computer Vision and adapts [Ivan Ludvig](https://ivanludvig.github.io/blog/2019/07/20/calculating-screen-to-face-distance-android
) research paper to detect if distance from webcam to computer screen is healthly (>24 inches). User will recieve windows toast notification if distance detected is consistantly less than threshold (<24 inches). Comes with two configuration methods (*Choose one*),
1. One time configuration - Measure distance from webcam to user using a ruler. Record the measured distance and displayed distance shown in the application (*Displayed distance will vary from measured distance during configuration)*. It is recommended to use a ruler pointing straight outward from your webcam to your eye level. 
2. Requires sensor size of the webcam you are currently using. *Varies from webcam manufacturer*

Currently supports Windows only, created by Winston Qian

#### Table of Contents
**[Project Usage](#usage)** <br>
**[Project Creation Process](#creation)** <br>
**[Future Improvements](#improve)** <br>
**[Resources](#resources)** <br>

## <a name = "usage"></a> Project Usage:
```
pip install -r requirements.txt
```
Contains two files to run application:
  1. main.py - For developers to run CLI, see main.py for commands
  2. gui.py - To run PyQt GUI for application


## <a name = "creation"></a> Project Creation Process:
Overuse of my eyes over quarrentine inspired me to 

## <a name="improve"></a> Future Improvements:
Eye detection for glasses could be improved (use better detection algorithm than haarcascades eyeglasses) 
Package into desktop application
Enable usage on MacOS 

## <a name="resources"></a> Resources

*ReadME in progress* 

