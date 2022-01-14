#!/usr/bin/env python3

# bare-bones-flask-ajax.py
# WESmith 01/12/22
# created a bare-bones example of flask and ajax


#import os
from flask import Flask, render_template, request, jsonify
#from flask import url_for, session
from datetime import datetime

#basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

default_button = ['DEFAULT', 0]

buttons = {'INVERT': {'on': 1, 'off': 2},
           'DEFOCUS':{'on': 3, 'off': 4},
           'FLIP':   {'on': 5, 'off': 6}}

button_vals = {'0': 'DEFAULT', 
               '1': 'INVERT ON',  '2': 'INVERT OFF',
               '3': 'DEFOCUS ON', '4': 'DEFOCUS OFF',
               '5': 'FLIP ON',    '6': 'FLIP OFF'}

@app.route('/')
def index():
    return render_template('working-demo-index.html',
                           default=default_button,
                           buttons=buttons)

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
    #print('\n\n IN BUTTON_RESULT \n\n')
    if request.method == "POST":
        result_txt = request.form['button_value']
        print('button value: {}'.format(result_txt))
        return jsonify(output=button_vals[result_txt])
        #return ''

if __name__ == "__main__":

    app.run(debug=True)

