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
from flask_paginate import Pagination, get_page_args

import numpy as np
import cv2
import  imutils
import sys
import pytesseract
import pandas as pd
import time

engine = create_engine('sqlite:///usersDb.db', echo=True)
UPLOAD_FOLDER = 'C:/xampp/htdocs/emergencyAlertForACrash/data/'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mkv', 'mpg', 'flv', 'mov', 'wmv', 'webm', '3gp'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
@app.route('/home/', methods=['GET', 'POST'])
def home():
    if not session.get('logged_in'):
        return render_template('login.php')
    else:
        frames = visualize_frame_from_video_valid()
        return render_template('index.php', results=frames)

@app.route('/login/', methods=['POST'])
def login():
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]))
    result = query.first()
    if result:
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()

@app.route('/logout/')
def logout():
    session['logged_in'] = False
    return home()

def get_results(offset=0, per_page=10):
    duree, result = investigate_crash()
    return result[offset: offset + per_page], result, duree

@app.route('/detection/')
def detection():
    return render_template('detection.php')

@app.route('/crashDetection/', methods=["GET", "POST"])
def crash_detection():
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    pagination_users, result, duree = get_results(offset=offset, per_page=per_page)
    total = len(result)
    print('total : ', total)
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
    frame = request.form.get('frame')
    if request.method == 'GET' and frame:
        return redirect(url_for('recognizePlate', frame=frame)) #, img=img
    return render_template('detection_result.php',
                           results=pagination_users,
                           duration=duree,
                           users=pagination_users,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )
@app.route('/accuracy/')
def accuracy_test():
    return render_template('accuracy.php')

@app.route('/performance/', methods=["GET", "POST"])
def performance():
    accuracy, duration = test()
    return render_template('accuracy.php', accuracy=accuracy, duration=duration)

@app.route("/videoBtn/", methods=["GET", "POST"])
def findVideo():
    if request.method == "POST":
        frames = visualize_frame_from_video_valid()
        return render_template('detection.php', results=frames)
    else:
        frames = visualize_frame_from_video_valid()
        return render_template('detection.php', results=frames)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload/', methods=['GET', 'POST'])
def upload_file():
    try:
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return redirect(url_for('uploaded_file',filename=filename))
        frames = visualize_frame_from_video_valid()
        return render_template('detection.php', results=frames)
    except:
        frames = visualize_frame_from_video_valid()
        return render_template('detection.php', results=frames)
    finally:
        frames = visualize_frame_from_video_valid()
        return render_template('detection.php', results=frames)


@app.route('/video/', methods=['GET', 'POST'])
def videos():
    result = request.form
    vid = result['url']
    youtube = pytube.YouTube(vid)
    video = youtube.streams.first()
    video.download('C:/xampp/htdocs/emergencyAlertForACrash/data/')
    #frames = visualize_frame_from_video_valid()
    return render_template('detection.php', src=vid)

@app.route('/lpr/')
def lpr():
    frame = request.args.get('frame', None)
    return render_template('lpr.php', frame=frame) #, img=img

@app.route('/recognizePlate/', methods=['GET', 'POST'])
def recognizePlate():
    result = request.form
    frame = result['frame']
    pytesseract.pytesseract.tesseract_cmd = (r"C:\Program Files\Tesseract-OCR\tesseract")
    strImg = 'static/generated_frames_valid/'+frame
    image = cv2.imread(strImg)
    #image = imutils.resize(image, width=500) #, width=500
    cv2.imshow("Original Image", image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    # cv2.imshow("2 - Bilateral Filter", gray)
    edged = cv2.Canny(gray, 170, 200)
    # cv2.imshow("4 - Canny Edges", edged)
    cnts, new = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:30]
    NumberPlateCnt = None
    count = 0
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:
            NumberPlateCnt = approx
            break
    # Masking the part other than the number plate
    mask = np.zeros(gray.shape, np.uint8)
    new_image = cv2.drawContours(mask, [NumberPlateCnt], 0, 255, -1)
    new_image = cv2.bitwise_and(image, image, mask=mask)
    cv2.namedWindow("Final_image", cv2.WINDOW_NORMAL)
    cv2.imshow("Final_image", new_image)
    # Configuration for tesseract
    config = ('-l eng --oem 1 --psm 3')
    # Run tesseract OCR on image
    text = pytesseract.image_to_string(new_image, config=config)
    # Data is stored in CSV file
    raw_data = {'date': [time.asctime(time.localtime(time.time()))], 'v_number': [text]}
    df = pd.DataFrame(raw_data, columns=['date', 'v_number'])
    df.to_csv('data.csv')
    # Print recognized text
    print(text)
    cv2.waitKey(0)
    #frame = request.args.get('frame', None);print('img crash detection : {},{}', img, frame)
    return render_template('lpr.php', res=text, frame=frame)

@app.route('/alert/')
def alert():
    return render_template('alert.php')

@app.route('/emergency/', methods=['GET', 'POST'])
def emergency():
    return render_template('alert.php')

@app.route('/urgence/', methods=['GET', 'POST'])
def urgence():
    try:
        subprocess.call(r'C:\WINDOWS\system32\cmd.exe /C "C:\Users\ASUS\AppData\Local\CounterPath\X-Lite\Current\X-Lite.exe"')
    except:
        subprocess.call(r'C:\WINDOWS\system32\cmd.exe /C "C:\Users\ASUS\AppData\Local\CounterPath\X-Lite\Current\X-Lite.exe"')
    finally:
        subprocess.call(r'C:\WINDOWS\system32\cmd.exe /C "C:\Users\ASUS\AppData\Local\CounterPath\X-Lite\Current\X-Lite.exe"')
    return render_template('alert.php')

@app.errorhandler(404)
@app.errorhandler(401)
@app.errorhandler(500)
def page_not_found(error):
    return render_template('error.php', code=error.code)

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0', port=5000)