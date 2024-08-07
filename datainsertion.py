import firebase_admin

from firebase_admin import credentials,db


cred = credentials.Certificate("serviceAccountKey.json")

firebase_admin.initialize_app(cred,{
    'databaseURL':"https://faceattendance-6c972-default-rtdb.firebaseio.com/"
})

ref = db.reference('Students')

data = {
    "22CSR001":{
        "name":"ELONMUSK",
        "MAJOR":"CSE",
        "regulation":2022,
        "Total_attendance":6,
        "last_attendance":"2024-05-05 00:54:34",
        "year":2
    }
}

for key,value in data.items():
    ref.child(key).set(value)