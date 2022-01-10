#!/usr/bin/python3

# url_for__demo.py
# WESmith 01/09/22 see readme.txt for source, WS modified for python 3

from flask import Flask, redirect, url_for

app = Flask(__name__)

@app.route('/admin')
def hello_admin():
    return 'hello admin'

@app.route('/guest/<guest>')
def hello_guest(guest):
    return 'hello {} as guest'.format(guest)

@app.route('/user/<name>')
def hello_user(name):
   if name =='admin':
      return redirect(url_for('hello_admin'))
   else:
      return redirect(url_for('hello_guest', guest = name))


if __name__ == '__main__':
    
   app.run(host='0.0.0.0', debug = True)