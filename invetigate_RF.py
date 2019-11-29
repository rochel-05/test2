from extract_frames_from_video import load_data_valid, extract_frames_from_video_valid
from extract_frames_from_video import load_data_train, load_data_test, load_data_train_raw
from os import listdir
from pickle import load
from keras.utils import to_categorical
import os, shutil
import datetime, json
import glob
import numpy as np
import pandas as pd
from sklearn import linear_model
from joblib import dump, load
import time
from flask import Flask
from flask import render_template
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from model_RF import RFClassifierModel
import matplotlib.pyplot as plt

app = Flask(__name__)

listInt = []
def getIndex(YList):
    index = 0
    #print("YList : ", YList)
    for data in YList[0]:
        #data = int(data)
        if data == 1:
            retour = index
        else:
            index += 1
    listInt.append(retour)
    return retour

def investigate_crash():
    startTime = time.time()
    # define categorical label
    label_dict = {
        0: 'Without Crash',
        1: 'Crash',
        2: 'Ambiguity Event',
        3: 'Unknwon Event',
        4: 'Unknown Event',
    }

    #load heterogenous data
    file3 = "diana.mp4"#"epic.mp4"
    srcDir = "C:/xampp/htdocs/emergencyAlertForACrash/data/"  #C:/wamp/www/emergencyAlertForACrash/data/"
    for elt in os.listdir("C:/xampp/htdocs/emergencyAlertForACrash/"):
        if elt.__eq__('crash_resultNew.json'):
            os.remove("C:/xampp/htdocs/emergencyAlertForACrash/" + elt)
            print("Deletion crash_resultNew.json file with sucess!!!")

    extract_frames_from_video_valid(srcDir) #extract_frames_from_video_valid(srcDir + file3)
    #print("removing file into home directory with success")
    Xtest = load_data_valid()
    print('input image shape : {}'.format(Xtest.shape))
    Xtest = np.reshape(Xtest, (-1, 150528))
    print('input image shape : {}'.format(Xtest.shape))

    # call model
    RFClassifier = load(open("model/RFClassifier_train3.pkl", "rb"))

    # evaluate
    predicted = RFClassifier.predict(Xtest)
    predict_cat = to_categorical(predicted, num_classes=5)
    predict_cat = predict_cat.astype('int')
    print("predicted : ", predict_cat)
    print("predict[0] : ", predict_cat[0])
    print("predict[4] : ", predict_cat[4])
    print('predict class shape : {}'.format(predict_cat.shape))
    # print('right class shape : {}'.format(Y_test.shape))
    # show result
    i = 0
    cota = 0
    with open("C:/xampp/htdocs/emergencyAlertForACrash/crash_resultNew.json", "a") as fichier:  #C:/wamp/www/emergencyAlertForACrash/crash_result.json

        now = datetime.datetime.now()
        daty = now.strftime("%d-%m-%Y")
        ora = now.strftime("%Hh:%Mm:%Ss")
        listJson = []
        i = 0
        fichier.write('{"VideoResults": [')

        for frame in listdir("static/generated_frames_valid/"):
            res = label_dict[getIndex(predict_cat[i])]
            frameK = frame
            print("frame : {}, crash found : {}".format(frame, res))

            frame = frame.split(".")[0]
            frameId = frame.split("d")[1]
            frameId = int(frameId)
            data = {'frame': frameK, 'resultat': res, 'zone': 1,'date': daty, 'heure': ora}
            listJson.append(data)

            try:
                if res.__eq__(label_dict[getIndex(predict_cat[1])]):
                    print("crash detected in frame n° :", frameId, "(" + frame + ".jpg)")
                    cota += 1
            except:
                print("il ya une erreur non prise en charge par le system")
            finally:
                i += 1
        i = 0
        while (i < len(listJson)):
            json.dump(listJson[i], fichier)
            if (i == len(listJson) - 1):
                pass
            else:
                fichier.write(",")
            i += 1
        fichier.write("]}")
        #predictions = RFClassifier.predict(Xtest)
        #print("number of accident found in this video ", predictions[0].shape[0])
        #print("number of scenario without accident found in this video ", predictions[1].shape[0])
        #print("number of ambigious scenary in this video ", predictions[2].shape[0])
        endTime = time.time()
        duree = endTime-startTime
        print('time consuming : ', duree, "s")
        return duree, listJson

def agregation_of_heterogenous_datas(Xtrain2, Ytrain2, Xtrain3, Ytrain3, Xtest2, Ytest2, Xtest3, Ytest3):
    #just comment and uncomment the lines if you choose to train only mongo data with csv data or mongo with raw
    Xtrain = np.append(Xtrain2, Xtrain3, axis=0)
    #Xtrain = np.append(Xtrain, Xtrain3, axis=0)

    Xtest = np.append(Xtest2, Xtest3, axis=0)
    #Xtest = np.append(Xtest, Xtest3, axis=0)

    Ytrain = np.append(Ytrain2, Ytrain3, axis=0)
    #Ytrain = np.append(Ytrain, Ytrain3, axis=0)

    Ytest = np.append(Ytest2, Ytest3, axis=0)
    #Ytest = np.append(Ytest, Ytest3, axis=0)

    print(' Xtrain shape : {} - Ytrain shape : {}'.format(Xtrain.shape, Ytrain.shape))
    print(' Xtest shape : {} - Ytest shape : {}'.format(Xtest.shape, Ytest.shape))
    return Xtrain, Ytrain, Xtest, Ytest

def test():
    startTime = time.time()
    #load heterogenous data
    #Xtrain1, Xtest1, Ytrain1, Ytest1 = load_data_train()
    #print('X_train1 shape : {}, X_test1 shape : {}'.format(Xtrain1.shape, Xtest1.shape))
    #print('Y_train1 shape : {}, Y_test1 shape : {}'.format(Ytrain1.shape, Ytest1.shape))
    Xtrain2, Xtest2, Ytrain2, Ytest2 = load_data_test()
    print('X_train2 shape : {}, X_test2 shape : {}'.format(Xtrain2.shape, Xtest2.shape))
    print('Y_train2 shape : {}, Y_test2 shape : {}'.format(Ytrain2.shape, Ytest2.shape))
    Xtrain3, Xtest3, Ytrain3, Ytest3 = load_data_train_raw()
    print('X_train3 shape : {}, X_test3 shape : {}'.format(Xtrain3.shape, Xtest3.shape))
    print('Y_train3 shape : {}, Y_test3 shape : {}'.format(Ytrain3.shape, Ytest3.shape))

    #agregate data with numpy
    Xtrain, Ytrain, Xtest, Ytest = agregation_of_heterogenous_datas(Xtrain2, Ytrain2, Xtrain3, Ytrain3, Xtest2, Ytest2, Xtest3, Ytest3)

    # call model
    RFClassifier = RFClassifierModel()
    RFClassifier.fit(Xtrain, Ytrain)
    # evaluate
    predicted = RFClassifier.predict(Xtest)
    accuracy = str(accuracy_score(Ytest, predicted) * 100)
    print('accuracy : {}%'.format(accuracy))
    endTime = time.time()
    duration = endTime - startTime
    return accuracy, duration

def visualize_frame_from_video_valid():
    listImg = []
    listFrames = []
    i = 0
    j = 0
    for img in os.listdir('static/generated_frames_valid'):
        print(img)
        listImg.append(img)
        i += 1
    while(j<10):
        if(len(listImg)!=0):
            listFrames.append(listImg[j])
        else:
            pass
        j += 1

    #img = plt.imread("generated_frames_valid/valid0.jpg")
    #plt.imshow(img)
    #plt.show()
    return listFrames

#visualize_frame_from_video_valid()