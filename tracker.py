# Here i will be tracking the ball which will be acting as a controller for the game
# Further the ball will be used to move the character in various different directions.
import cv2
import imutils
from pynput.keyboard import Key, Controller
keyboard=Controller()

greeLow=(29,86,6)
greenUP=(64,255,255)

cap=cv2.VideoCapture(0)

while(True):
    ret,frame=cap.read()

    # Converting the frame to hsv
    frame=imutils.resize(frame,width=600)
    blurred=cv2.GaussianBlur(frame,(11,11),0)
    frame_HSV=cv2.cvtColor(blurred,cv2.COLOR_BGR2HSV)

    # masking with greencolor
    mask=cv2.inRange(frame_HSV,greeLow,greenUP)
    mask=cv2.erode(mask,None,iterations=2)
    mask=cv2.dilate(mask,None,iterations=2)

    # cv2.imshow('frame',cv2.flip(frame_HSV,1))
    # cv2.imshow('frame',cv2.flip(mask,1))

    cnts=cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts=imutils.grab_contours(cnts)
    center=None

    if(len(cnts))>0:
        c=max(cnts,key=cv2.contourArea)
        ((x,y),radius)=cv2.minEnclosingCircle(c)
        M=cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # Drawing the rectangle
        cv2.rectangle(frame,(150,150),(375,375),color=greeLow,thickness=2)

        # Triggering the keys
        if int(x)>375 and 50<int(y)<375:
            print("left")
            keyboard.press('a')
            keyboard.release('a')
        elif int(x)<150 and 50<int(y)<375:
            print("right")
            keyboard.press('d')
            keyboard.release('d')
        elif 150<int(x)<375 and int(y)<150:
            print("top")
            keyboard.press('w')
            keyboard.release('w')
        elif 150<int(x)<375 and int(y)>375:
            print("Bottom")
            keyboard.press('s')
            keyboard.release('s')
        else:
            print("stable")

        # Drawing the circle
        if radius>10:
            cv2.circle(frame,(int(x),int(y)),int(radius),(0,255,255),2)
            cv2.circle(frame,center,5,(0,0,255),-1)
    cv2.imshow('frame',cv2.flip(frame,1))


    # Breaking out of the loop
    if cv2.waitKey(20) & 0xFF==ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
