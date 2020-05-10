# B.Tech final year project
 Developed and tested in Linux environment.Might work with other platforms but never tested
 The prerequsite for this program to run are flask,flask-socketio, opencv-python and face recongintion which can be installed by executing the follow pypi using `pip3`(or `pip2` for Python2):
 
     pip3 install  opencv-python flask flask-socketio

 The face_recongintion  is quite tricky to install so the guides to install them for Linux,mac are [here](https://gist.github.com/ageitgey/629d75c1baac34dfa5ca2a1928a7aeaf) and for Windows is [here](https://github.com/ageitgey/face_recognition/issues/175#issue-257710508)

 For executing the application you need to run the app.py program with python3 
    python app.py
 You can acess the application homepage either by enterning `https://localhost:8000(default path)` in your browser or you can acess from another device using the IP address of the system which running the application.If all went well you will see `Hello World` in your browser.

 You need to open the path `/camera` to make it a client camera that records the data.

 The `/dashboard`  will be the place where you can view the recorded data in the real-time
 
 To add the images you need can save it into the pictures folder or use the in-built path `/save` 