import cv2
import os
from datetime import date
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import joblib
from website import app
import datetime as dt

#### Saving Date today in 2 different formats
def datetoday():
    return date.today().strftime("%m_%d_%y")
def datetoday2():
    return date.today().strftime("%d-%B-%Y")

#open cam
face_detector = cv2.CascadeClassifier('face_detection/haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

#create attendance file
if not os.path.isdir('Attendance'):
    os.makedirs('Attendance')
if not os.path.isdir('face_detection/faces'):
    os.makedirs('face_detection/faces')
if f'Attendance-{datetoday}.csv' not in os.listdir('Attendance'):
    x = date.today()
    with open(f'Attendance//Attendance-{x.day}-{x.month}-{x.year}.csv','w') as f:
        f.write('Name,ID,Time')

# get a number of total registered users
def totalreg():
    return len(os.listdir('face_detection/faces'))


# extract the face from an image to make a training set
def extract_faces(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)     #make the face gray
    face_points = face_detector.detectMultiScale(gray, 1.3, 5)
    return face_points


# Identify face using ML(machine learning) model 

def identify_face(facearray):
    model = joblib.load('face_detection/face_recognition_model.pkl')
    return model.predict(facearray)


# make training set 
def train_model():
    faces = []    #save faces in array
    labels = []   #save names in array
    userlist = os.listdir('face_detection/faces')
    for user in userlist:
        for imgname in os.listdir(f'face_detection/faces/{user}'):
            img = cv2.imread(f'face_detection/faces/{user}/{imgname}')
            resized_face = cv2.resize(img, (50, 50))
            faces.append(resized_face.ravel())
            labels.append(user)
    faces = np.array(faces)
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(faces,labels)
    joblib.dump(knn,'face_detection/face_recognition_model.pkl')

# Extract info from today's attendance file in attendance folder
def extract_attendance():
    df = pd.read_csv(f'Attendance/Attendance-{x.day}-{x.month}-{x.year}.csv')
    names = df['Name']
    IDs = df['ID']
    times = df['Time']
    l = len(df)
    return names,IDs,times,l
# save faces
# face recognition
# Add Attendance of a specific user
def add_attendance(name):
    username = name.split('_')[0]
    userid = name.split('_')[1]
    current_time = dt.datetime.now().strftime("%H:%M:%S")
    
    df = pd.read_csv(f'Attendance/Attendance-{x.day}-{x.month}-{x.year}.csv')
    if int(userid) not in list(df['ID']):
        with open(f'Attendance/Attendance-{x.day}-{x.month}-{x.year}.csv','a') as f:
            f.write(f'\n{username},{userid},{current_time}')


