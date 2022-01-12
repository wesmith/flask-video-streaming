#!/usr/bin/env python3

# flask-demo-qt-interval.py
# WESmith 01/11/22
# copied from
# https://towardsdatascience.com/
# using-python-flask-and-ajax-to-pass-information-between-the-client-and-server-90670c64d688


import os
from flask import Flask, render_template, url_for, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

''' # WS turn off db stuff
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,
                                                                    'qtdata.db')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)

class Store_QTc_data(db.Model):
    __tablename__ = 'qt_data'
    id         = db.Column('id', db.Integer, primary_key = True)
    timestamp  = db.Column('timestamp', db.DateTime)
    QTc        = db.Column('QTc', db.Integer)
    prolonged  = db.Column('prolonged', db.String(50))
    heart_rate = db.Column('heart rate', db.Integer)
    QT         = db.Column('QT', db.Integer)
    sex        = db.Column('sex', db.CHAR)

    def __init__(self, QTc, prolonged, heart_rate, QT, sex):
        self.QTc = QTc
        self.prolonged = prolonged
        self.timestamp = datetime.now()
        self.heart_rate = heart_rate
        self.QT = QT
        self.sex = sex
'''

@app.route('/')
def index():
    print('\n\nhello from index()\n\n')  # WS
    #if not os.path.exists(os.path.join(basedir, 'qtdata.db')):
    #    db.create_all()
    return render_template('index.html')


@app.route('/WS_test', methods=['POST', 'GET'])
def test():
    print('\n\nin /WS_test route')
    print('\n\nrequest = {}\n\n'.format(request.args))
    #for j, k in request.args.get('key').iteritems:
    #    print(j, k)
    #print(dd)
    return jsonify(output='it worked!')  # this works
    #output = request
    #return output

@app.route('/process_qtc', methods=['POST', 'GET'])
def process_qt_calculation():
    print('\n\nhello from process_qt_calculation()\n\n')  # WS

    if request.method == "POST":
        qtc_data = request.get_json()

        print('\n\nqtc_data: {}\n\n'.format(qtc_data)) # WS

        ''' # WS turn off all db stuff
        db.session.add(Store_QTc_data(qtc_data[0]['QTc'],
                                      qtc_data[1]['prolonged'],
                                      qtc_data[2]['HR'],
                                      qtc_data[3]['QT'],
                                      qtc_data[4]['Sex']))
        db.session.commit()
        rows = db.session.query(Store_QTc_data).count()
        '''
    rows = 5 # WS
    results = {'rows': rows}
    return jsonify(results)


if __name__ == "__main__":

    app.run(debug=True)

