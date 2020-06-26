# --------------------------------------------------------
# Camera sample code for Jetson Nano
#
# This program could capture and display video from
# IP CAM
#
#
# IP address 
# Change your stream IP link according to your requirements
# rtsp://rcb:password123@192.168.1.250:80
# 
# Note: press ESC Key to close 
# Modified from Jk Jung's Code
# Credits to https://jkjung-avt.github.io/tx2-camera-with-python/

import sys
import subprocess

import cv2

WINDOW_NAME = 'Camera Demo'
# Change your stream IP link according to your requirements
uri = 'rtsp://rcb:password123@192.168.1.250:80'
width = 1280
height = 720
latency = 100

# read rtsp stream
def open_cam_rtsp(uri, width, height, latency):
    gst_str = ('rtspsrc location={} latency={} ! '
               'rtph264depay ! h264parse ! omxh264dec ! '
               'nvvidconv ! '
               'video/x-raw, width=(int){}, height=(int){}, '
               'format=(string)BGRx ! '
               'videoconvert ! appsink').format(uri, latency, width, height)
    return cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER)

#Open output window
def open_window(width, height):
    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(WINDOW_NAME, width, height)
    cv2.moveWindow(WINDOW_NAME, 0, 0)
    cv2.setWindowTitle(WINDOW_NAME, 'Camera Demo for Jetson Nano')

# RUN RTSP Stream
def main():
    print('OpenCV version: {}'.format(cv2.__version__))
    help_text = '"Esc" to Quit, "H" for Help, "F" to Toggle Fullscreen'
    font = cv2.FONT_HERSHEY_PLAIN
    cap = open_cam_rtsp(uri, width, height, latency)

    if not cap.isOpened():
        sys.exit('Failed to open camera!')
    

    while True:
        open_window(width,height)
        _, img = cap.read() # grab the next image frame from camera
        cv2.putText(img, help_text, (11, 20), font,
                        1.0, (32, 32, 32), 4, cv2.LINE_AA)
        cv2.imshow(WINDOW_NAME, img)

        key = cv2.waitKey(10)
        if key == 27: # ESC key: quit program
            break
        
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()