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
from flask import jsonify, request

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
           'BLUR':   {'on': 3, 'off': 4},
           'FLIP':   {'on': 5, 'off': 6},
           'GRAY':   {'on': 7, 'off': 8}}

class Message():
    def __init__(self):
        self.value   = '0'
        self.mapping = {'0': 'DEFAULT', 
                        '1': 'INVERT ON', '2': 'INVERT OFF',
                        '3': 'BLUR ON',   '4': 'BLUR OFF',
                        '5': 'FLIP ON',   '6': 'FLIP OFF',
                        '7': 'GRAY ON',   '8': 'GRAY OFF'}
msg = Message()

app = Flask(__name__)

@app.route('/')
def index():
    """Video streaming home page."""
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

@app.route('/button_input', methods=['POST', 'GET'])
def button_inputs():
    # update the message to the Camera class from button inputs
    if request.method == "POST":
        result_txt = request.form['button_value']
        msg.value = result_txt
        #print('button value: {}'.format(result_txt))
        return jsonify(output=msg.mapping[msg.value])   

@app.route('/video_feed')
def video_feed():
    """
    Video streaming route. Put this in the src attribute of an
    img tag.
    """
    txt = 'multipart/x-mixed-replace; boundary=frame'
    # WS added passing a message to the Camera class
    return Response(gen(Camera(message=msg)), mimetype=txt)


if __name__ == '__main__':
    # WS added debug for automatic reloading
    app.run(host='0.0.0.0', threaded=True, debug=True)
