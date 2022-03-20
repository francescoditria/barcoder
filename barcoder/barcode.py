#libraries
#pip install Pillow
#pip install opencv-python
#pip install pyzbar

import cv2 
import time
import winsound
import os
from pyzbar.pyzbar import decode
from datetime import datetime

#bar-code-reader 
title = "Registering attendances"
valid_codes_file = "valid_codes.csv"
record_file = "record.csv"    
ok_file = "ok.wav"
error_file = "error.wav" 


cap=cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
time.sleep(1)
 
#open file of valid codes
valid_codes=[]
f = open(valid_codes_file,"r")
for x in f:
    print("valid code",x.rstrip())
    valid_codes.append(str(x.rstrip()))
    

n = len(valid_codes)
if n>0:   
    print("ready")
    camera = True
else:
    print("No valid codes")
    camera = False

file_object = open(record_file, 'a')
while camera == True:
    success, frame = cap.read()
    
    for code in decode(frame):
        os.system('cls' if os.name=='nt' else 'clear')
        #print
        print(code.type,code.data.decode('utf-8'))
        if str(code.data.decode('utf-8')) in valid_codes:
            print("ok")
            #beep
            #winsound.Beep(440, 500)
            winsound.PlaySound(ok_file, winsound.SND_FILENAME)
            #timestamp
            now = datetime.now()
            timestamp = datetime.timestamp(now)
            date_time = datetime.fromtimestamp(timestamp)
            d = date_time.strftime("%m/%d/%Y,%H:%M:%S")
            #save to csv
            record=d+","+code.type+","+code.data.decode('utf-8')+"\n"
            file_object.write(record)
        else:
            print("error: code not found")
            winsound.PlaySound(error_file, winsound.SND_FILENAME)
            #winsound.Beep(2500, 1000)    
        #delay
        time.sleep(2)
                   
        
    cv2.imshow(title,frame)
    cv2.waitKey(1)
    if cv2.getWindowProperty(title, cv2.WND_PROP_VISIBLE) < 1:    
        camera = False

print("Terminating program")
file_object.close()
cap.release()
cv2.destroyAllWindows()
    
    
    