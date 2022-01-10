#!/usr/bin/python3

# WS_example.py
# WESmith 01/10/22 
# create example buttons that transfer information


from flask import Flask, render_template

app = Flask(__name__)

msg = {'on': 1, 'off': 0}

@app.route('/')
@app.route('/<value>')
def index(value=0):
    print('value from button is: {}'.format(value))
    return render_template("index.html", msg=msg)

if __name__ == '__main__':
    
    app.run(debug = True)
