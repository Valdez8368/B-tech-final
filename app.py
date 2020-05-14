from flask import Flask,render_template
from flask_socketio import SocketIO,emit
import face_recognition
import numpy as np
import os
import cv2
from time import time
app = Flask(__name__)
app.config['SECRET_KEY']='kite!'
socketio=SocketIO(app)
known_faces=[]
known_names=[]
devices={}
path='pictures'
start=time()
@app.route("/")
def hello():
    return "Hello World!"
@app.route("/front")
def frontCamera():
    return render_template('test.html')
@app.route('/back')
def backCamera():
    return render_template('camera.html')
@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html')
@app.route('/save')
def save():
    return render_template('save.html')
@socketio.on('camera')
def handler(message):
    print(message[0])
    if message[0] not in devices:
        devices[message[0]]={}
    image=uri2image(message[1])
    face_framed=face_rec(message[0],image)
    data=image2uri(face_framed)
    devices[message[0]]['data']=data
    sendData()
@socketio.on('save')
def saveImage(message):
    from urllib import request
    response=request.urlopen(message[1])
    f=open(os.path.join(path,message[0]+'.png'),'wb')
    f.write(response.file.read())
    f.close()
def sendData():
    from json import dumps
    data=dumps(devices,sort_keys=True)
    print(len(devices))
    socketio.emit('video',data)
    if((time()-start)>10):
        devices.clear()
def image2uri(image):
    from PIL import Image
    from io import BytesIO
    from base64 import b64encode
    img=Image.fromarray(cv2.cvtColor(image,cv2.COLOR_BGR2RGB))
    data=BytesIO()
    img.save(data,"png")
    data64=b64encode(data.getvalue())
    return u'data:img/png;base64,'+data64.decode('utf-8')
def uri2image(uri):
    import base64
    data=uri.split(',')[1]
    decoded_data=base64.b64decode(data)
    np_data=np.fromstring(decoded_data,np.uint8)
    img=cv2.imdecode(np_data,cv2.IMREAD_UNCHANGED)
    return img

def face_rec(device,frame):
    frame_rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    locations=face_recognition.face_locations(frame_rgb)
    encoding=face_recognition.face_encodings(frame_rgb,locations)
    match=''
    for face_encoding,face_location in zip(encoding,locations):
        results=face_recognition.compare_faces(known_faces,face_encoding,0.4)
        print(results)
        if True in results:
            match=known_names[results.index(True)]
            print(f'-{match}')
            color=(0,0,255)
            top_left=(face_location[3],face_location[0])
            bottom_right=(face_location[1],face_location[2])
            cv2.rectangle(frame,top_left,bottom_right,color,3)
            top_left=(face_location[3],face_location[2])
            bottom_right=(face_location[1],face_location[2]+22)
            cv2.rectangle(frame,top_left,bottom_right,color,cv2.FILLED)
            cv2.putText(frame,match,(face_location[3]+10,face_location[2]+15),cv2.FONT_HERSHEY_SIMPLEX,0.5,(200,200,200),2)
    devices[device]['found']=match
    return frame

if __name__ == "__main__":
    for i in os.listdir(path):
        image=face_recognition.load_image_file(os.path.join(path,i))
        encoding=face_recognition.face_encodings(image)
        known_faces.append(encoding)
        known_names.append(i.split('.')[0])
    socketio.run(app,host='0.0.0.0',port=8000,ssl_context='adhoc')
