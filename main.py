#!/home/phil/bin/python

import cv2

vido = cv2.VideoCapture(0)

while(True):
    try:
        er0, frame0 = vido.read()
        er1, frame1 = vido.read()
        er2, frame2 = vido.read()
    except e:
        print(e)
    
    img = frame0.copy()
    imghsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    cv2.imshow('converting to HSV', imghsv)
    cv2.imshow('Frame0', frame0)
    cv2.imshow('Frame1', frame1)
    cv2.imshow('frame2', frame2)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        vido.release()
        print("catching exit by X")
        cv2.destroyAllWindows()
vido.release()
cv2.destroyAllWindows()
