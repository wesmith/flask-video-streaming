#!/usr/bin/python3

# WS_example.py
# WESmith 01/10/22 
# create example buttons that transfer information


from flask import Flask, render_template

app = Flask(__name__)

buttons = {'INVERT': {'on': 0, 'off': 1},
           'DEFOCUS':{'on': 2, 'off': 3},
           'FLIP':   {'on': 4, 'off': 5}}

class Message():
    def __init__(self):
        self.mapping = {'0': 'INVERT ON',  '1': 'INVERT OFF',
                        '2': 'DEFOCUS ON', '3': 'DEFOCUS OFF',
                        '4': 'FLIP ON',    '5': 'FLIP OFF'}
msg = Message()

@app.route('/')
@app.route('/<value>')
def index(value=None):
    print('value from button press: {}'.\
          format(msg.mapping[value]))
    return render_template("index.html", buttons=buttons)

if __name__ == '__main__':
    
    app.run(debug = True)
