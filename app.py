#!/usr/bin/env python3

# WESmith 01/07/22 this worked with the simulated camera out
# of the box: impressive

# WS TODO
# - run webcam via opencv
# - add command-line inputs: camera type, url, port

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

app = Flask(__name__)

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

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
    return Response(gen(Camera()), mimetype=txt)


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
