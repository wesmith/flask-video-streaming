#!/usr/bin/env python3

# working-demo-flask-ajax.py
# WESmith 01/15/22
# created a bare-bones example of flask and ajax


from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

default_button = ['DEFAULT_VALUES', 0]

invert = {'INVERT_COLORS': {'YES': 10, 'NO': 11}}
flip   = {'FLIP_IMAGE':{'HORIZ': 20, 'VERT': 21,
                        '180_DEG': 22}}
gray   = {'GRAYSCALE': {'YES': 30, 'NO': 31}}
blur   = {'BLUR':      {'TURN_OFF': 41}}

button_vals  = {'0': 'DEFAULT',
               '10': 'INVERT ON',  '11': 'INVERT OFF',
               '20': 'FLIP HORIZ', '21': 'FLIP VERT',
               '22': 'FLIP 180 DEG',
               '30': 'GRAYSCALE',   '31': 'COLOR',
               '41': 'NO BLURRING', '42': 'BLURRING ON'}

@app.route('/')
def index():
    return render_template('working-demo-index.html',
                           default=default_button,
                           invert=invert,
                           flip=flip,
                           gray=gray,
                           blur=blur)

@app.route('/WS_test', methods=['POST', 'GET'])
def test():
    if request.method == "POST":
        result_txt = request.form['data']
        txt  = result_txt.split(',')
        vals = [float(k) for k in txt]
        res  = sum(map(float, vals))
        return jsonify(output='it worked! got {} at {}'.\
                       format(res, datetime.now()))
    else:
        print('\n\nrequest method was not POST\n\n')
        return jsonify(output='POST method not used')
    
@app.route('/button_result', methods=['POST', 'GET'])
def button_result():
    if request.method == "POST":
        result_txt = request.form['button_value']
        print('button value: {}'.format(result_txt))

        # WS '999' is the symbol to indicate blurring-kernel size input
        if result_txt[-3:] == '999':
            val = result_txt[:-3] # strip off the symbol
            print('val: {}'.format(val))
            ttt = 'Blurring with kernel size {} x {}'.format(val, val)
            print(ttt)
            return jsonify(output=ttt)
        else:
            return jsonify(output=button_vals[result_txt])


if __name__ == "__main__":

    app.run(debug=True)

