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

@app.route('/')
def index():
    return render_template('working-demo-index.html')

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


if __name__ == "__main__":

    app.run(debug=True)

