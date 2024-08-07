import cv2,cvzone
import os
import pickle
import face_recognition,numpy
import firebase_admin
from firebase_admin import credentials,storage,db
import numpy as np
from datetime import datetime
cred = credentials.Certificate("serviceAccountKey.json")

firebase_admin.initialize_app(cred,{
    'databaseURL':"https://faceattendance-6c972-default-rtdb.firebaseio.com/",
    'storageBucket':"faceattendance-6c972.appspot.com"
})

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

bucket = storage.bucket()
background = cv2.imread('Resources/background.png')

modeType = 0
counter =0
id=-1
imgstd =[]
folderModePath ='Resources/Modes'
pathlist = os.listdir(folderModePath)
imgModeList=[]
for path in pathlist:
    imgModeList.append(cv2.imread(os.path.join(folderModePath,path)))

file = open('encode.p','rb')
knowndetails=pickle.load(file)
file.close()
knowimglist,stdid = knowndetails

while True:
    success, img = cap.read()
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)

    face = face_recognition.face_locations(imgS)
    encodeface =face_recognition.face_encodings(imgS,face)
    
    background[162:162+480,55:55+640]=img
    background[44:44+633,808:808+414]=imgModeList[modeType]
    if face:
        for enf,f in zip(encodeface,face):
            matches = face_recognition.compare_faces(knowimglist,enf)
            facedistance = face_recognition.face_distance(knowimglist,enf)
            matchIndex = numpy.argmin(facedistance)
            if matches[matchIndex]:
                y1,x2,y2,x1 =f
                y1,x2,y2,x1 =y1*4,x2*4,y2*4,x1*4
                bbox=x1+55,y1+162,x2-x1,y2-y1
                background=cvzone.cornerRect(background,bbox,rt=0)
                id = stdid[matchIndex]
                if counter==0:
                    cvzone.putTextRect(background,"Loading",(275,400))
                    cv2.imshow("Face Attendance",background)
                    cv2.waitKey(1)
                    counter=1
                    modeType=1
        if counter!=0:
            if counter==1:
                stdinfo = db.reference(f'Students/{id}').get()
                print(stdinfo)
                blob = bucket.get_blob(f"images/{id}.png")
                array = np.frombuffer(blob.download_as_string(),np.uint8)
                imgstd = cv2.imdecode(array,cv2.COLOR_BGRA2BGR)
                datetimeobj = datetime.strptime(stdinfo['last_attendance'],"%Y-%m-%d %H:%M:%S")
                secondElapsed=(datetime.now()-datetimeobj).total_seconds()
                if secondElapsed>2700:
                    ref = db.reference(f'Students/{id}')
                    stdinfo['Total_attendance']+=1
                    ref.child('Total_attendance').set(stdinfo['Total_attendance'])
                    ref.child('last_attendance').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    modeType =3
                    conter=0
                    background[44:44+633,808:808+414]=imgModeList[modeType]
            if 15<counter<25 and modeType!=3:
                modeType=2
            background[44:44+633,808:808+414]=imgModeList[modeType]
    
            if counter<=15 and modeType!=3:
                cv2.putText(background,str(stdinfo['Total_attendance']),(861,125),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
                cv2.putText(background,str(stdinfo['MAJOR']),(1006,550),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
                cv2.putText(background,str(id),(1006,493),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
                cv2.putText(background,str(stdinfo['year']),(1025,625),cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1)
                cv2.putText(background,str(stdinfo['regulation']),(1125,625),cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1)


                (w,h),_=cv2.getTextSize(stdinfo['name'],cv2.FONT_HERSHEY_COMPLEX,1,1)
                offest = (414-w)//2
                cv2.putText(background,str(stdinfo['name']),(808+offest,445),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
                background[175:175+216,909:909+216]=imgstd
            counter+=1
            if counter>=25:
                counter=0
                modeType=0
                stdinfo=[]
                imgstd =[]
                background[44:44+633,808:808+414]=imgModeList[modeType]
    else:
        modeType=0
        counter=0
   

    cv2.imshow("Face Attendance",background)
    cv2.waitKey(1)