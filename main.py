import argparse

from face_recognition import face_recognition
from calibration_cam import calibration

def main():
    calibration.calibrate()
    parser = argparse.ArgumentParser()
    parser.add_argument("--display-image", action="store_true", help="Display Detected Image")
    args = parser.parse_args()

    face_recognition(args.display_image)
    

if __name__ == '__main__':
    main()