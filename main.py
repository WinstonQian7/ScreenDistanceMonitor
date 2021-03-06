#Developers only/use cmd prompt for testing 
import argparse

#local modules
import processing
from processing.distance_processing import runDetection 
from calibration_cam.calibration import calibrate

#default args: no display img, 5 second cooldown between notifications, distance not displayed, adj = 0
#Recommended ex: py main.py -d -i
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--display-image","-d", action="store_true", help="Display grayscale detection of eyes")
    parser.add_argument("--cooldown", "-c", type=int,default=5,help="cooldown period between notifications and detection will not run")
    parser.add_argument("--cooldown-second-minute", "-s", action="store_false", help="Option to switch cooldown period from minutes to seconds" )
    parser.add_argument("--info","-i", action="store_true", help="prints if eyes are being detected and distance from screen")
    parser.add_argument("--adjustment-factor","-adj", type=float,default=0,
                help="Adjustment factor(+/-) used to correct distances on different devices, use if sensor size and focal length is unknown")
    args = parser.parse_args()

    runDetection(args.display_image,args.cooldown,
        args.cooldown_second_minute,args.info,args.adjustment_factor)
    

if __name__ == '__main__':
    main()