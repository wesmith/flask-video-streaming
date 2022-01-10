#!/usr/bin/python3

# template_loop__demo.py
# WESmith 01/09/22 
# see readme.txt for source, WS modified for python 3


from flask import Flask, render_template

app = Flask(__name__)

@app.route('/result')
def result():
    dict = {'phys':50,'chem':60,'math':70}
    
    return render_template('result.html', result = dict)

if __name__ == '__main__':
    
    app.run(debug = True)