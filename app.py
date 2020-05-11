#importing the required modules
from flask import Flask,render_template
from flask_socketio import SocketIO,emit
import face_recognition
import numpy as np
import os
import cv2
#initialization of variables
app = Flask(__name__)
app.config['SECRET_KEY']='kite!'
socketio=SocketIO(app)
known_faces=[]
known_names=[]
path='pictures'

#setting response to the url paths
@app.route("/")
def hello():
    return "Hello World!"
@app.route("/camera")
def newCamera():
    return render_template('test.html')
@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html')
@app.route('/save')
def save():
    return render_template('save.html')
@socketio.on('camera') #getting the image as base64
def handler(message): 
    image=uri2image(message) #changing the base64 to image object
    face_framed=face_rec(image) #performing face recognition on the image
    data=image2uri(face_framed) #again changing the image object to base64 
    socketio.emit('video',data) #sending it to the dashboard
@socketio.on('save')    #saving an image file for now needs restrating of the server to get it online
def saveImage(message):
    from urllib import request
    response=request.urlopen(message[1])    
    f=open(os.path.join(path,message[0]+'.png'),'wb')
    f.write(response.file.read())
    f.close()

#function for image to uri/base64 data
def image2uri(image): 
    from PIL import Image
    from io import BytesIO
    from base64 import b64encode
    img=Image.fromarray(cv2.cvtColor(image,cv2.COLOR_BGR2RGB))
    data=BytesIO()
    img.save(data,"png")
    data64=b64encode(data.getvalue())
    return u'data:img/png;base64,'+data64.decode('utf-8')

#function for uri to image object
def uri2image(uri):
    import base64
    data=uri.split(',')[1]
    decoded_data=base64.b64decode(data)
    np_data=np.fromstring(decoded_data,np.uint8)
    img=cv2.imdecode(np_data,cv2.IMREAD_UNCHANGED)
    return img
#function for the face recognition module
def face_rec(frame):
    frame_rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    locations=face_recognition.face_locations(frame_rgb)
    encoding=face_recognition.face_encodings(frame_rgb,locations)
    for face_encoding,face_location in zip(encoding,locations):
        results=face_recognition.compare_faces(known_faces,face_encoding)
        match=None
        if True in results:
            match=known_names[results.index(True)]
            print(f'-{match}')
        #putting the fancy box thing around the face
        color=(0,0,255)
        top_left=(face_location[3],face_location[0])
        bottom_right=(face_location[1],face_location[2])
        cv2.rectangle(frame,top_left,bottom_right,color,3)
        top_left=(face_location[3],face_location[2])
        bottom_right=(face_location[1],face_location[2]+22)
        cv2.rectangle(frame,top_left,bottom_right,color,cv2.FILLED)
        cv2.putText(frame,match,(face_location[3]+10,face_location[2]+15),cv2.FONT_HERSHEY_SIMPLEX,0.5,(200,200,200),2)

    return frame
#main function to start the server and encoding the images stored in the folder
if __name__ == "__main__":
    for i in os.listdir(path):
        image=face_recognition.load_image_file(os.path.join(path,i))
        encoding=face_recognition.face_encodings(image)
        known_faces.append(encoding)
        known_names.append(i.split('.')[0])
    socketio.run(app,host='0.0.0.0',port=8000,ssl_context='adhoc')
