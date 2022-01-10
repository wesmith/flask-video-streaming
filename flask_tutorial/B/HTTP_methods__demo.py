#!/usr/bin/python3

# HTTP_methods__demo.py
# WESmith 01/09/22 
# see readme.txt for source, WS modified for python 3

# WS NOTE: to run this example, it is necessary to tell the
# browser explicitly where the login.html file is:
# 1) add this url to the browser (assuming this is still the
#    correct location of login.html):
#  file:///home/pi/Devel/raspberry_pi/flask-video-streaming/
#  flask_tutorial/B/login.html
# 2) start the server below, and click 'submit', and you get
#    the 'welcome' page; if the server isn't running, you get
#    an error

from flask import Flask, redirect, url_for, request

app = Flask(__name__)

@app.route('/success/<name>')
def success(name):
    return 'welcome %s' % name

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        print('WS mod: POST selection')
        user = request.form['nm']
        return redirect(url_for('success',name = user))
    else:
        print('WS mod: not-POST selection')
        user = request.args.get('nm')
        for i, j in request.args.items(): # WS print to term
            print('key: {}, value: {}'.format(i, j))
        return redirect(url_for('success',name = user))

if __name__ == '__main__':

    #app.run(host='0.0.0.0', debug = True)
    
    # runs 'localhost' as default
    app.run(debug=True)