import cv2
import numpy as np
import os
import time
import database as send

def fungsirecognetion():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('trainer/trainer.yml')
    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath);
    font = cv2.FONT_HERSHEY_SIMPLEX

    #iniciate id counter
    id = 0
    # names related to ids: example
    names = ['None','Azis', 'Umam', 'Anto']

    # Initialize and start realtime video capture
    cam = cv2.VideoCapture(0)
    cam.set(3, 640) # set video widht
    cam.set(4, 480) # set video height

    # Define min window size to be recognized as a face
    minW = 0.1*cam.get(3)
    minH = 0.1*cam.get(4)
    counter=0
    servo=1
    while True:
        ret, img =cam.read()
        #img = cv2.flip(img, -1) # Flip vertically
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        cl1=clahe.apply(gray)
        faces = faceCascade.detectMultiScale(
            cl1,
            scaleFactor = 1.2,
            minNeighbors = 5,
            minSize = (int(minW), int(minH)),
           )
        for(x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
            id, confidence = recognizer.predict(cl1[y:y+h,x:x+w])
            hasil=confidence
            cv2.imshow('camera',img)
            if(confidence<37):
                kecocokan="{0}%".format(round(100-confidence))
                print("cocok", kecocokan)

                nama=names[id]
                waktu=time.asctime(time.localtime(time.time()))
                print (waktu)

                #sending to database
                send.postmongo(nama, kecocokan, waktu)
                send.fungsiThingboard(id)
                servo=1
                print("buka kunci", names[id])

                #tutup camera
                print("\n [INFO] Exiting Program and cleanup stuff")
                cam.release()
                cv2.destroyAllWindows()
                return servo
            else:
                kecocokan="{0}%".format(round(100-confidence))
                print("tidak cocok")
                counter=counter+1
                if(counter==15):
                    kecocokan="{0}%".format(round(100-confidence))
                    idmaling=0
                    nama="maling"

                    waktu=time.asctime(time.localtime(time.time()))
                    print (waktu)

                    send.postmongo(nama, kecocokan, waktu)
                    send.fungsiThingboard(idmaling)
                    print("kunci pintu")
                    servo=0
                    #tutup camera
                    print("\n [INFO] Exiting Program and cleanup stuff")
                    cam.release()
                    cv2.destroyAllWindows()
                    return servo

        k = cv2.waitKey(delay=20) # Press 'ESC' for exiting video
        if k == 27:
            break

    print("\n [INFO] Exiting Program and cleanup stuff")
    cam.release()
    cv2.destroyAllWindows()
