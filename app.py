#!/usr/bin/env python3

# WESmith 01/07/22 this worked with the simulated camera out
# of the box: impressive

# WS TODO
# - (done) run webcam via opencv
# - add command-line inputs: camera type, url, port, frame size
# - apply a stylesheet
# - generalize camera to support image-processing algorithms


from importlib import import_module
import os
from flask import Flask, render_template, Response

# import camera driver
if os.environ.get('CAMERA'):
    Camera = import_module('camera_' +\
                           os.environ['CAMERA']).Camera
else:
    from camera import Camera

# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera

default_button = ['DEFAULT', 0]

buttons = {'INVERT': {'on': 1, 'off': 2},
           'DEFOCUS':{'on': 3, 'off': 4},
           'FLIP':   {'on': 5, 'off': 6}}

class Message():
    def __init__(self):
        self.value   = '0'
        self.mapping = {'0': 'DEFAULT', 
                        '1': 'INVERT ON',  '2': 'INVERT OFF',
                        '3': 'DEFOCUS ON', '4': 'DEFOCUS OFF',
                        '5': 'FLIP ON',    '6': 'FLIP OFF'}
msg = Message()

app = Flask(__name__)

@app.route('/')
@app.route('/<value>') # WS added buttons
def index(value=0):
    """Video streaming home page."""
    msg.value = str(value)
    #print('\nvalue from button press: {}\n'.\
    #      format(msg.mapping[msg.value]))
    return render_template('index.html',
                           default=default_button,
                           buttons=buttons)

def gen(camera):
    """Video streaming generator function."""
    yield b'--frame\r\n'
    while True:
        frame = camera.get_frame()
        yield b'Content-Type: image/jpeg\r\n\r\n' + frame +\
              b'\r\n--frame\r\n'
        
@app.route('/video_feed')
def video_feed():
    """
    Video streaming route. Put this in the src attribute of an
    img tag.
    """
    txt = 'multipart/x-mixed-replace; boundary=frame'
    # WS try passing a message to Camera class
    return Response(gen(Camera(message=msg)), mimetype=txt)


if __name__ == '__main__':
    # WS added debug for automatic reloading
    app.run(host='0.0.0.0', threaded=True, debug=True)
