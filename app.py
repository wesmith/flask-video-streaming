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

button_names = ['ZERO', 'ONE', 'TWO']  # WS

class Message():
    def __init__(self, msg=100):
        self.msg = msg
msg = Message()

app = Flask(__name__)

@app.route('/')
@app.route('/val') # WS added buttons
def index(val=5):
    """Video streaming home page."""
    msg.msg = val
    return render_template('index.html',
                           buttons=button_names)

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
