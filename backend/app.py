from flask import Flask,jsonify,request
import firebase_admin
from firebase_admin import credentials,firestore,storage
import cv2
import base64
import requests
import io
import numpy as np
import datetime  
import random
from PIL import Image
import pyrebase
import os

def convert(string,name):

    image = base64.b64decode(str(string))       
    fileName = name

    imagePath = "/home/learner/Desktop/app2/backend/images/" + fileName

    img = Image.open(io.BytesIO(image))
    img.save(imagePath, 'jpeg')
    return fileName


app = Flask(__name__)

cred = credentials.Certificate('serviceAccount.json')

firebase_admin.initialize_app(cred)

config = {
    "apiKey": "AIzaSyDCHQLRGASmP2PhgQY0RAeCu2kn6B8c21Y",
    "authDomain": "fishapp-122bc.firebaseapp.com",
    "projectId": "fishapp-122bc",
    "databaseURL": "https://fishapp-122bc-default-rtdb.firebaseio.com/",
    "storageBucket": "fishapp-122bc.appspot.com",
    "messagingSenderId": "997413319923",
    "appId": "1:997413319923:web:3397d9ddbd9f4e28db3386",
    "measurementId": "G-CRGEX1F1X9"
}


firebase = pyrebase.initialize_app(config)

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()

db = firestore.client()

# Document for userAccounts
userAccounts  = db.collection('userAccounts')
userCatches = db.collection('userCatches')
adminUpdates = db.collection('adminUpdates')
#The base route - This usually is used to check whether server is up or not.
@app.route('/')
def index():
    return "Hello World"

@app.route('/signup',methods=['POST'])
def signup():

    data = request.json
    print(data)
    try:
        getMobileNo = str(data['mobileNo'])
        # We get the user
        user = userAccounts.document(getMobileNo).get().to_dict()
        if user != None:
            return {"success":False,"details":"Mobile Number Already Exists"}
        else:
            # Creating the account details in firebase
            userAccounts.document(getMobileNo).set(data)
            response = jsonify({"success":True})
            return response
    except Exception as e:
        return f"An Error Occured: {e}",400




@app.route('/postAnUpdate',methods=['POST'])
def postUpdate():

    data  = request.json
    print(data)
    try:
        current_time = datetime.datetime.now() 
        updateId = ''.join([str(random.randint(0, 999)).zfill(3) for _ in range(2)])
        date = '/'.join([str(current_time.day),str(current_time.month),str(current_time.year)])
        time = ':'.join([str(current_time.hour),str(current_time.minute),str(current_time.second)])
        data['updateTime'] = time
        data['updateDate'] = date
        data['updateId'] = updateId
        adminUpdates.document(updateId).set(data)
        response = jsonify({"success":True}),200
        return response
    except Exception as e:
        return f"An Error Occured", 500


@app.route('/getAllUpdates',methods=['GET'])
def getAllUpdates():
    try:
        updates = adminUpdates.stream()
        updatesArray = list()
        for update in updates:
            temp = update.to_dict()
            updatesArray.append(temp)
        print(updatesArray)
        return jsonify({'success':True,'updatesArray':updatesArray}), 200

    except Exception as e:
        return f"An error occured", 500

'''

    #How will a particular catch look like.
    {
        "image":"imageUrl",
        "date":date,
        "name":name,
        "weight":weight,
    }

'''

#We need to show the users catches.
@app.route('/getCatchesHistory',methods=['GET'])
def getCatches():
    print("hi")
    data = request.args
    print(data)
    try:
        mobile = str(data['mobile'])
        print(mobile)
        catchDetails = userCatches.document(mobile).get().to_dict()["catches"]
        print(catchDetails)
        return jsonify({"success":True,"catches":catchDetails})
    except Exception as e:
        return f"An error occured {e}", 400


@app.route('/updateCatch',methods=['POST'])
def updateCatch():

    try:
        data  = request.json
        print(data)
        print(data['image'])
        convert(data['image'],data['imageFileName'])
        imagePath = "/home/learner/Desktop/app2/backend/images/" + data['imageFileName']
        
        storage.child('fishes/{}'.format(data['imageFileName'])).put(imagePath)
        fish_url = storage.child('fishes/{}'.format(data['imageFileName'])).get_url(None)
        data = {
            'date':data['date'],
            'description':data['description'],
            'image':fish_url,
            'latitude':data['latitude'],
            'longitude':data['longitude'],
            'name':data['name'],
            'weight':data['weight'],
            'number':data['number']
        }
        ref = userCatches.document(str(data['number']))
        ref.update({u'catches': firestore.ArrayUnion([data])})
        return jsonify({"success":True})
    
    except Exception as e:
        return jsonify({"success":False}), 400


@app.route('/login',methods=['POST'])
def login():

    data = request.json
    print(data)

    try:
        getMobileNo = str(data['mobile'])
        user = userAccounts.document(getMobileNo).get().to_dict()
        print(user)
        if user == None:
            return {"success":False,"details":"Mobile Number Not Registered"}
        else:
            print("hi")
            passwordSent = data['password']
            actualPassword = user['password']
            print(passwordSent,actualPassword)
            if passwordSent == actualPassword:
                user['success'] = True
                response = jsonify(user)
                return response
            else:
                response = jsonify({"success":False,"details":"Invalid Password"})
                return response
    
    except Exception as e:
        return f"An error Occured: {e}",400

if __name__ == "__main__":
    app.run(debug=True)