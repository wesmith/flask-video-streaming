#!/usr/bin/python3

# static__demo.py
# WESmith 01/09/22 
# see readme.txt for source, WS modified for python 3


from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == '__main__':
    
    app.run(debug = True)
