import os
import cv2
from base_camera import BaseCamera
import datetime  # WS
import rpi_status as ws  #WS

def add_info(frame): # WS
    timestamp = datetime.datetime.now()
    txt = timestamp.strftime("%d %B %Y %I:%M:%S %p")
    cv2.putText(frame,
                txt,
                (20, frame.shape[0] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.90,
                (255, 120, 255), 2)
    temp = ws.get_temp()
    temp = '{}: {}'.format(*temp)
    cv2.putText(frame, temp, (20, frame.shape[0] - 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.90,
                (0, 255, 255), 2)
    uptime = ws.get_uptime()
    uptime = '{}: {}'.format(*uptime)
    cv2.putText(frame, uptime, (20, frame.shape[0] - 70),
                cv2.FONT_HERSHEY_SIMPLEX, 0.90,
                (255, 255, 120), 2)
    return frame

class Camera(BaseCamera):
    video_source = 0

    def __init__(self):
        if os.environ.get('OPENCV_CAMERA_SOURCE'):
            val = int(os.environ['OPENCV_CAMERA_SOURCE']) # WS
            Camera.set_video_source(val) # WS: shorten line
        super(Camera, self).__init__()

    @staticmethod
    def set_video_source(source):
        Camera.video_source = source

    @staticmethod
    def frames():
        camera = cv2.VideoCapture(Camera.video_source)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        # sizes: 640x480, 352x288, 320x240, 176x144, 160x120
        # need to verify and get a complete list WS
        camera.set(cv2.CAP_PROP_FRAME_WIDTH,  640)  # WS
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # WS

        while True:
            # read current frame
            _, img = camera.read()

            # image processing step goes here
            # xxx

            # information as text on image goes here
            img = add_info(img)  # WS

            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img)[1].tobytes()
