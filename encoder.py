import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials,storage


cred = credentials.Certificate("serviceAccountKey.json")

firebase_admin.initialize_app(cred,{
    'databaseURL':"https://faceattendance-6c972-default-rtdb.firebaseio.com/",
    'storageBucket':"faceattendance-6c972.appspot.com"
})
folderPath  = 'images'
modepathlist = os.listdir(folderPath)
imglist=[]
stdid=[]
for path in modepathlist:
    imglist.append(cv2.imread(os.path.join(folderPath,path)))
    stdid.append(os.path.splitext(path)[0])
    fileName = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)

def findEncodings(imglist):
    encodelist=[]
    for img in imglist:
        img =cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodelist.append(encode)
    return encodelist
print("encoding starts....")
knownlist = findEncodings(imglist)
knowndetails = [knownlist,stdid]
print("encodingends...")
file = open('encode.p','wb')
pickle.dump(knowndetails,file)
file.close()