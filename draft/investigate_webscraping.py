from keras.models import load_model
from extract_frames_from_video import load_data_valid, extract_frames_from_video_valid, extract_frames_from_video_valid_scraping
from os import listdir
from keras.utils import to_categorical
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import json
import pytube

#define variables and chrome driver
home_dir = "C:\\Users\\ASUS\\PycharmProjects\\vehicle_accident_investigation_flask"
now = datetime.datetime. now()
listInt = []
driver = webdriver.Chrome(home_dir + "\\chrome_driver\\chromedriver.exe")
url = "https://www.youtube.com/results?search_query=vehicle+crash+in+a+traffic+road"

def getIndex(YList):
    index = 0
    #print("YList : ", YList)
    for data in YList:
        #data = int(data)
        #print("data : ", data)
        if data == 1:
            retour = index
        else:
            index += 1
    listInt.append(retour)
    return retour

def get_YouTube_Data_Using_Web_Scraping():
    driver.get(url)
    user_data = driver.find_elements_by_xpath('//*[@id="thumbnail"]')
    links = []
    for i in user_data:
        links.append(i.get_attribute('href'))
    print("we have found ", len(links), "video data concerning traffic road accident on youtube")

    # create a dataframe with 4 columns (link, title, description, category) to store video details
    df_accident = pd.DataFrame(columns=['link', 'title', 'description', 'category'])

    # scrape video details in youtube
    wait = WebDriverWait(driver, 10)
    v_category = "CATEGORY_NAME"
    i = 0
    listUrl = []
    for x in links:
        try:
            print("x : " + str(i), x)  # url
            # x = str(x)
            driver.get(x)
            v_id = x.strip('https://www.youtube.com/watch?v=')
            v_title = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.title yt-formatted-string"))).text
            v_description = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#description yt-formatted-string"))).text
            df_accident.loc[len(df_accident)] = [v_id, v_title, v_description, v_category]
            listUrl.append(x)
        except:
            print("Invalid url format")
        i += 1

    # merge data into single dataframe
    frames = [df_accident]
    df_copy = pd.concat(frames, axis=0, join='outer', join_axes=None, ignore_index=True, keys=None, levels=None,names=None, verify_integrity=False, copy=True)

    df_link = pd.DataFrame(columns=["link"])
    df_title = pd.DataFrame(columns=["title"])  # title
    df_description = pd.DataFrame(columns=["description"])  # description
    df_category = pd.DataFrame(columns=["category"])
    df_link["link"] = df_copy['link']
    df_title["title"] = df_copy['title']
    df_description["description"] = df_copy['description']
    df_category["category"] = df_copy['category']
    #print("df_link : ", df_link)
    #print("df_title : ", df_title)  # title
    #print("df_description : ", df_description)  # description
    #print("df_category : ", df_category)
    return listUrl, df_title, df_description

def investigate_crash2():
    # define categorical label
    label_dict = {
        0: 'Without Crash',
        1: 'Crash',
        2: 'Ambiguity Event',
        3: 'Unknwon Event',
        4: 'Unknown Event',
    }
    #load data
    listUrl, df_title, df_description = get_YouTube_Data_Using_Web_Scraping()
    youtube = pytube.YouTube(listUrl[0])
    video = youtube.streams.first()
    video.download('C:/xampp/htdocs/emergencyAlertForACrash/data/')
    extract_frames_from_video_valid('C:/xampp/htdocs/emergencyAlertForACrash/data/')
    X_test1 = load_data_valid()
    print('input image shape : {}'.format(X_test1.shape))

    #call model
    vehicle_crash_investigator_model = load_model(home_dir + '\\model\\VAICS_epoch1010int.h5py')

    #predict label category rely for the input image
    predict = vehicle_crash_investigator_model.predict(X_test1)
    print("predicted : ", predict)
    predict_cat = to_categorical(predict, num_classes=5)
    predict_cat = predict_cat.astype('int')
    print("predicted : ", predict_cat)

    # show result
    i = 0
    listFrameNames = []
    listResults = []

    for frame in listdir(home_dir+"\\static\\generated_frames_valid\\"):
        res = label_dict[getIndex(predict_cat[i])]
        listFrameNames.append(frame)
        listResults.append(label_dict[getIndex(predict_cat[i])])
        try:
            if res.__eq__(label_dict[getIndex(predict_cat[1])]):
                frame = frame.split(".")[0]
                frameId = frame.split("d")[1]
                frameId = int(frameId)
                print("crash detected in frame n° :", frameId, "(" + frame + ".jpg)")
        except:
            print("Error05 :cet erreur n'est pas prise en charge par le systeme")
        finally:
            i+=1

if __name__=="__main__":
    investigate_crash2()