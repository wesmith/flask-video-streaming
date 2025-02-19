#!/usr/bin/python3

# template__demo.py
# WESmith 01/09/22 
# see readme.txt for source, WS modified for python 3

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/hello/<int:score>')
def hello_name(score):
    return render_template('hello.html', marks = score)

if __name__ == '__main__':
    
    app.run(debug = True)
