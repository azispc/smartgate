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
    #eyeCascade = cv2.CascadeClassifier('haarcascade_eye.xml')

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

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor = 1.2,
            minNeighbors = 5,
            minSize = (int(minW), int(minH)),
           )

        for(x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
            id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
            hasil=confidence
            #cv2.imshow('camera',img)
            ''''
            if (confidence < 37):
                id = names[id]
                confidence_per = "  {0}%".format(round(100-confidence))
                cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
                cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)
            else:
                id = "Bukan"
                confidence_per = "  {0}%".format(round(100-confidence))
                cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
                cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)'''
                
        print("confidence: ", hasil)
        if(confidence < 37):
            kecocokan="{0}%".format(round(100-confidence))
            print(" {0}%".format(round(100-confidence)))

            nama=names[id]
            print("buka kunci", names[id])

            #print("Kirim Data Waktu!")

            waktu=time.asctime(time.localtime(time.time()))
            print (time.asctime( time.localtime(time.time()) ))

            send.postmongo(nama, kecocokan, waktu)
            send.fungsiThingboard(id)
            servo=1
            return servo
            break

        else:
            print(" {0}%".format(round(100-confidence)))
            print("kunci pintu")
            counter=counter+1
            if(counter==15):
                kecocokan="{0}%".format(round(100-confidence))
                idmaling=0
                nama="maling"

                print("kunci pintu")
                #print("kirim notifikasi pemilik rumah")
                waktu=time.asctime(time.localtime(time.time()))
                print (time.asctime( time.localtime(time.time()) ))
                send.postmongo(nama, kecocokan, waktu)
                send.fungsiThingboard(idmaling)
                servo=0
                return servo
                break

        k = cv2.waitKey(delay=20) # Press 'ESC' for exiting video
        if k == 27:
            break

    print("\n [INFO] Exiting Program and cleanup stuff")
    cam.release()
    cv2.destroyAllWindows()
