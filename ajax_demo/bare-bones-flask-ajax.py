#!/usr/bin/env python3

# bare-bones-flask-ajax.py
# WESmith 01/12/22
# created a bare-bones example of flask and ajax


#import os
from flask import Flask, render_template, request, jsonify
#from flask import url_for, session
#from datetime import datetime

#basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('indexOne.html')
'''
@app.route('/WS_test', methods=['POST', 'GET'])
def test():
    if request.method == "POST":
        data = request.get_json()
        for k in data:
            print('/n/nResults in back end:')
            print(k)
        return jsonify(output='it worked!') 
    else: 
        print('request method was not POST')
        return jsonify(output='did not get data')  
'''

if __name__ == "__main__":

    app.run(debug=True)

