from cv2 import cv2
import mediapipe as mp
import time
import os
import numpy as np

brushThickness = 22
eraserThickness = 90

cap=cv2.VideoCapture(1)
mpHands=mp.solutions.hands
hands=mpHands.Hands()
mpDraw= mp.solutions.drawing_utils

tipIds= [4,8,12,16,20]
 
drawColor = (30, 255, 255)
xp, yp = 0, 0
imgCanvas = np.zeros((480, 640, 3), np.uint8)

def Hand_Finder(img,draw=True):
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            if draw:
                mpDraw.draw_landmarks(img, handLms,mpHands.HAND_CONNECTIONS)
    return img

def Finger_Detector(img,handNo=0,draw=True):
    landmark_List=[]
    if results.multi_hand_landmarks:
        myHand=results.multi_hand_landmarks[handNo]

        for id, lm in enumerate(myHand.landmark):
            h,w,c =img.shape
            cx,cy =int(lm.x*w),int(lm.y*h)
            landmark_List.append([id,cx,cy])
            if draw:
                cv2.circle(img,(cx,cy),5,(255,0,255),cv2.FILLED)
    return landmark_List

def finger_Counter():

        fingers = []
        # Thumb
        if landmark_List[tipIds[0]][1] > landmark_List[tipIds[0]-1] [1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Fingers
        for id in range(1, 5):

            if landmark_List[tipIds[id]][2] < landmark_List[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        # totalFingers = fingers.count(1)
        return fingers

while(cap.isOpened()):
    success, img = cap.read()
    img = cv2.flip(img, 1)
    #print(img.shape) #480x640
    #convert the image BGR2RGB
    converted_image=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results=hands.process(converted_image)

    #Calling the hand finder 
    # pass captured img and results
    img=Hand_Finder(img)
    #Calling Finger Detector
    #pass captured img and results
    landmark_List=Finger_Detector(img,draw=False)
    #print(lmList)

    if len(landmark_List)!=0:  
        x1, y1 = landmark_List[8][1:]
        x2, y2 = landmark_List[12][1:]     
        fingers=finger_Counter()
        #print(fingers)
        if fingers[1] and fingers[2]:
            xp, yp = 0, 0
            #print('Selection Mode')
            #Checking for the click
            if y1 < 80:
                if 10 < x1 < 120:
                    drawColor = (255, 0, 255)
                elif 150 < x1 < 260:
                    drawColor = (255, 0, 0)
                elif 296 < x1 < 400:
                    drawColor = (0, 255, 0)
                elif 436 < x1 < 540:
                    drawColor = (0, 0, 0)
                elif 560 < x1 < 600:
                     imgCanvas_new=np.zeros((480, 640, 3), np.uint8)
                     imgCanvas=imgCanvas_new
                     #to clear the window

            cv2.rectangle(img, (x1, y1- 25), (x2, y2 + 25), drawColor, cv2.FILLED)
        
        if fingers[1] and fingers[2] == False and y1>78:
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
            #print("Drawing Mode") 
            if xp == 0 and yp == 0:
                xp,yp = x1, y1
            if drawColor == (0, 0, 0):
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
            else:
                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
            xp, yp = x1, y1

     
    cv2.rectangle(img, (10,10), (120,80), (255,0,255),cv2.FILLED)
    cv2.rectangle(img, (150,10), (260,80), (255,0,0),cv2.FILLED)
    cv2.rectangle(img, (296,10), (400,80), (0,255,0),cv2.FILLED)
    cv2.rectangle(img, (436,10), (540,80), (0,0,0),cv2.FILLED)
    cv2.rectangle(img, (560,10), (600,80), (255,255,255),cv2.FILLED)
    cv2.putText(img,'Clear',(560,50),cv2.FONT_HERSHEY_PLAIN,1,(0,0,255),2) 
    cv2.putText(img,'Ereaser',(450,50),cv2.FONT_HERSHEY_PLAIN,1,(255,255,255),2) 
    
    if(drawColor==(255, 0, 255)):
        cv2.putText(img,'Selected',(30,50),cv2.FONT_HERSHEY_PLAIN,1,(255,255,255),2)
    elif(drawColor == (255, 0, 0)):
        cv2.putText(img,'Selected',(170,50),cv2.FONT_HERSHEY_PLAIN,1,(255,255,255),2)
    elif(drawColor == (0, 255, 0)):
        cv2.putText(img,'Selected',(310,50),cv2.FONT_HERSHEY_PLAIN,1,(255,255,255),2)
    elif(drawColor == (0, 0, 0)):
        cv2.putText(img,'Selected',(450,50),cv2.FONT_HERSHEY_PLAIN,1,(255,255,255),2)    


    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    #cv2.imshow("Gray_Scale", imgGray)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    #cv2.imshow("Inverse_Image", imgInv)
    imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
    #cv2.imshow("New_Inv", imgInv)
    img = cv2.bitwise_and(img,imgInv)
    #cv2.imshow("and", img)
    img = cv2.bitwise_or(img,imgCanvas)
    #cv2.imshow("or", img)

    #Showing the window
    cv2.imshow("Virtual Painter",img)
    #cv2.imshow("Canvas", imgCanvas)
    if cv2.waitKey(1)==113:
        break
 
