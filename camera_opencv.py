import os
import cv2
from base_camera import BaseCamera


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

            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img)[1].tobytes()
