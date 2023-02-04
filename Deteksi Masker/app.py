
from flask import Flask, render_template, Response
import cv2
app=Flask(__name__)
camera = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_SIMPLEX


def gen_frames():  
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            face_cascade = cv2.CascadeClassifier("haarcascade/haarcascade_frontalface_default.xml")
            noseCascade = cv2.CascadeClassifier("haarcascade/Nariz.xml")
            mouth_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_mcs_mouth.xml')
            face_mask = cv2.CascadeClassifier("cascadedownload/cascade.xml")
            faces = face_cascade.detectMultiScale(frame, 1.1, 4)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
             #Draw the rectangle around each face
            if(len(faces) == 0):
                cv2.putText(frame,'Tidak Ada Orang',(250,50),font,1,(255,0,0),2)
            else :
                for (x, y, w, h) in faces:
            
                    mouth_rects = mouth_cascade.detectMultiScale(gray, 1.5, 5)
                    
                    nose_rects = noseCascade.detectMultiScale(gray, 1.5, 5)
                    
                    mask_rects = face_mask.detectMultiScale(gray, 1.5, 5)
                
                if(len(mouth_rects) == 0 and len(nose_rects) == 0):
                    cv2.putText(frame,'Menggunakan Masker',(170,50),font,1,(0,255,0),2)
                    cv2.putText(frame,'100%',(50,250),font,1,(250,255,0),2)
                    cv2.putText(frame,'Hidung Dan Mulut Tertutup',(150,450),font,1,(250,255,0),2)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0,255,0), 5)
                    
                    for (mx, my, mw, mh) in mask_rects:
                        if(y < my < y + h):
                            cv2.putText(frame,'Masker',(mx,my),font,0.5,(250,255,0),2)
                            cv2.rectangle(frame, (mx, my), (mx + mw, my + mh), (250,255,0), 2)
                            break
                
                elif(len(mouth_rects) == 0 and len(nose_rects) != 0):
                    cv2.putText(frame,'Pengunaan Masker Salah',(150,50),font,1,(0, 255, 255),2)
                    cv2.putText(frame,'50%',(50,250),font,1,(250,255,0),2)
                    cv2.putText(frame,'Hidung Tidak Tertutup',(150,450),font,1,(0, 0, 255),2)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0,255,255), 5)

                    for (mx, my, mw, mh) in nose_rects:
                        if(y < my < y + h):
                            cv2.rectangle(frame, (mx, my), (mx + mw, my + mh), (0, 0, 255), 2)
                            break
                    
                elif(len(mouth_rects) != 0 and len(nose_rects) == 0):
                    cv2.putText(frame,'Pengunaan Masker Salah',(150,50),font,1,(0, 251, 255),2)
                    cv2.putText(frame,'50%',(50,250),font,1,(250,255,0),2)
                    cv2.putText(frame,'Mulut tidak Tertutup',(150,450),font,1,(0, 0, 255),2)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0,255,255), 5)
                    
                    for (mx, my, mw, mh) in mouth_rects:
                        if(y < my < y + h):
                            cv2.rectangle(frame, (mx, my), (mx + mw, my + mh), (0, 0, 255), 2)
                            break
                    
                else:
                    for (mx, my, mw, mh) in mouth_rects:
                        if(y < my < y + h):
                            cv2.rectangle(frame, (mx, my), (mx + mw, my + mh), (0, 0, 255), 2)
                            break
                            
                    for (mx, my, mw, mh) in nose_rects:
                        if(y < my < y + h):
                            cv2.rectangle(frame, (mx, my), (mx + mw, my + mh), (0, 0, 255), 2)
                            break
                            
                    cv2.putText(frame,'Tidak Menggunakan Masker',(150,50),font,1,(0, 0, 255),2)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0,0,255), 5)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
if __name__=='__main__':
    app.run(debug=True)