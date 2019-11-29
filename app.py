import time
from flask import Flask
from flask import render_template, make_response
from flask import flash, Flask, redirect, render_template, request, session, abort, url_for
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker
from table import *
from test_accuracy_RF import test
from invetigate_RF import *
import os, subprocess
from werkzeug.utils import secure_filename
from string import Template
import pytube

engine = create_engine('sqlite:///usersDb.db', echo=True)
UPLOAD_FOLDER = 'C:/xampp/htdocs/emergencyAlertForACrash/data/'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mkv', 'mpg', 'flv', 'mov', 'wmv', 'webm', '3gp'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/detection/')
def crash_detection():
    duree, result = investigate_crash()
    frames = visualize_frame_from_video_valid()
    return render_template('indexA.html', title="Intelligent Crash Detection System (ICDS)", results=result, duration=duree, frames=frames) #, results=result, duration=duree

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0', port=8080)