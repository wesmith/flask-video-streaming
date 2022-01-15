import os
import cv2
from base_camera import BaseCamera
import datetime          # WS
import rpi_status as ws  # WS module
from time import time    # WS


def sec_to_dhms(sec): # seconds to day, hour, min, sec
    dd, r  = divmod(sec, 24*3600)
    hh, r  = divmod(r,      3600)
    mm, ss = divmod(r,        60)
    return 'Camera uptime: {} D, {} H, {} M, {:.1f} S'.\
            format(int(dd), int(hh), int(mm), ss)

def add_info(frame, fps, cam_uptime, scale, wid_hei, msg): # WS
    font   = cv2.FONT_HERSHEY_SIMPLEX
    f_size = 0.90 * scale
    separation = int(10 * scale)
    row0   = frame.shape[0] - separation
    col0   = 10
    delta  = int(30 * scale)
    thick  = 2 if scale >= 1 else 1

    timestamp = datetime.datetime.now()
    txt = timestamp.strftime("%d %B %Y %I:%M:%S %p")
    cv2.putText(frame, txt, (col0, row0), font, f_size,
                (255, 120, 255), thick) # light magenta
    temp = ws.get_temp()
    temp = '{}: {}'.format(*temp)
    cv2.putText(frame, temp, (col0, row0 - delta), font, f_size,
                (0, 255, 255), thick) # bright yellow
    #uptime = ws.get_uptime()  # system uptime
    #uptime = '{}: {}'.format(*uptime)
    uptime = sec_to_dhms(cam_uptime)
    cv2.putText(frame, uptime, (col0, row0 - 2 * delta), font, f_size,
                (255, 255, 120), thick) # light cyan
    fps = '{:4.1f} FPS for width {}, height {}'.format(fps, *wid_hei)
    cv2.putText(frame, fps, (col0, row0 - 3 * delta), font, f_size,
                (120, 255, 120), thick) # light green
    msg = 'Button message: {}'.format(msg)
    cv2.putText(frame, msg, (col0, row0 - 4 * delta), font, f_size,
                (255, 255, 255), thick) # white
    return frame

class Camera(BaseCamera):
    video_source = 0
    #message = None  # WS

    def __init__(self, message=None):
        if os.environ.get('OPENCV_CAMERA_SOURCE'):
            val = int(os.environ['OPENCV_CAMERA_SOURCE']) # WS
            Camera.set_video_source(val) # WS: shorten line
            
        Camera.message = message # WS
       
        super(Camera, self).__init__()
        
    @staticmethod
    def set_video_source(source):
        Camera.video_source = source
        
    @staticmethod
    def frames():
        cam = cv2.VideoCapture(Camera.video_source)
        if not cam.isOpened():
            raise RuntimeError('Could not start camera.')

        # WS some size options (not a complete list)
        # develop at 'large' or 'medium'
        size = 'large' #'medium'
        sizes = {'small':  ( 160, 120), # image too small
                 'medium': ( 320, 240), # ok for development
                 'large':  ( 640, 480), # ok for development
                 'Xlarge': (1280, 960)} # image too big
        scale = {'small': 0.25, 'medium': 0.50, 
                 'large': 1.00, 'Xlarge': 2.00}
        wid, hei = sizes[size]
        cam.set(cv2.CAP_PROP_FRAME_WIDTH,  wid)  # WS
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, hei)  # WS
        
        fps   = 15.0   # WS a rough initial value
        t_start = t_old = time() # WS
        # WS alpha: smoothing factor for frame/sec estimate,
        # float 0 to 1; the larger alpha, the more smoothing
        alpha = 0.9

        # processing flags
        INVERT = False
        BLUR   = False
        FLIP   = False
        
        while True:
            # WS calculate frames/sec (fps) in while loop
            dt    = time() - t_old
            t_old = time()
            fps   = alpha * fps + (1 - alpha) / dt
            cam_uptime = t_old - t_start  # time cam on in sec
            
            # read current frame
            _, img = cam.read()

            # get user's button-push from the web page
            msg = Camera.message
            
            # get processing flags
            if msg.value =='0':
                INVERT = BLUR = FLIP = False
            # invert colors
            if msg.value == '1': INVERT = True
            if msg.value == '2': INVERT = False
            # blur image with a fixed kernel size (will be an input later)
            if msg.value == '3': BLUR = True
            if msg.value == '4': BLUR = False
            # flip image left-right
            if msg.value == '5': FLIP = True
            if msg.value == '6': FLIP = False
            
            # image processing steps go here
            if INVERT: img = ~img
            if BLUR:   img = cv2.blur(img, (10, 10))
            # 0, 1, -1 to flip around vert, horiz, both axes, respectively
            if FLIP:   img = cv2.flip(img, 1)

            # add text on image after processing
            img = add_info(img, fps, cam_uptime,
                           scale[size], sizes[size],
                           msg.mapping[msg.value]) # WS

            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img)[1].tobytes()
