from keras.applications.vgg16 import VGG16
from keras.layers import Dense, InputLayer, Dropout
from extract_frames_from_video import load_data_train, load_data_test, load_data_train_raw
from model_RF import RFClassifierModel
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from flask import Flask
from flask import render_template
import time

app = Flask(__name__)

def reduction_of_dimension_with_PCA(Xtrain, Xtest):
    #standardize data with StandardScaler
    sc = StandardScaler()
    Xtrain = sc.fit_transform(Xtrain)
    Xtest = sc.transform(Xtest)
    #call pca function of sklearn
    pca = PCA()
    Xtrain = pca.fit_transform(Xtrain)
    Xtest = pca.transform(Xtest)
    return Xtrain, Xtest

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

if __name__ == '__main__':
    test()