import cv2
import mediapipe as mp
import HandTrackingModule as htm
import time
import math
import GestureVolumeControllerModule as gvc
import GestureBrightnessControllerModule as gbc

prevtime = 0
minPixelc = 25 #can set as per need
minPixelk = 20 #can set as per need

print("\n🔃 Opening Gesture Control Window 🔃\n")
vidcap = cv2.VideoCapture(0)
vidcap.set(3,640)
vidcap.set(4,480)

detectorobj = htm.HandDetector()
flag = 0

while True:
    ret, frameflip = vidcap.read()
    frame = cv2.flip(frameflip,1)
    frame = detectorobj.findHands(frame)
    lmList = detectorobj.findLoc(frame,draw=False)

    if flag!=2:
        cv2.rectangle(frame, (160,10), (390,70), (200,0,0), -1)
        cv2.putText(frame,"Adjust Volume",(197,47),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255),2)
    if flag!=1:
        cv2.rectangle(frame, (400,10), (630,70), (200,0,0), -1)
        cv2.putText(frame,"Adjust Brightness",(420,47),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255),2)

    if len(lmList)!=0:
        xi, yi = lmList[8][1], lmList[8][2]
        xt, yt = lmList[4][1], lmList[4][2]
        xm, ym = lmList[12][1], lmList[12][2]
        xr, yr = lmList[16][1], lmList[16][2]
        cxc, cyc = (xi+xt)//2, (yi+yt)//2
        netlengthc = math.hypot(xt-xi,yt-yi)
        if flag!=1 and flag!=2:
            cv2.circle(frame, (xi,yi), 10, (200,0,0), -1)
    
        if netlengthc<minPixelc and 160<xi<390 and 0<yi<75 or flag==1:
            flag = 1
            cv2.rectangle(frame, (160,10), (390,70), (0,150,0), -1)
            cv2.putText(frame,"Adjusting Volume",(183,47),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255),2)
            cv2.rectangle(frame, (100,10), (150,70), (0,0,150), -1)
            cv2.putText(frame,"<<",(109,47),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255),2)
            gvc.GVCfunc(frame,xt,yt,xr,yr,lmList)
            if 100<xr<150 and 0<yr<75:
                flag = 0                 
                
        if netlengthc<minPixelc and 400<xi<640 and 0<yi<75 or flag==2:
            flag = 2
            cv2.rectangle(frame, (400,10), (630,70), (0,150,0), -1)
            cv2.putText(frame,"Adjusting Brightness",(409,47),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255),2)
            cv2.rectangle(frame, (100,10), (150,70), (0,0,150), -1)
            cv2.putText(frame,"<<",(109,47),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255),2)
            gbc.GVBfunc(frame,xt,yt,xm,ym,lmList)
            if 100<xm<150 and 0<ym<75:
                flag = 0
        
    currtime = time.time()
    fps = 1/(currtime-prevtime)
    cv2.putText(frame,str(int(fps))+" FPS",(10,20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 200),2)
    prevtime = currtime
    cv2.putText(frame,"Press \"X\" to Exit Gesture Control Window",(300,468),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 200),2)

    cv2.imshow('Gesture Control Window', frame)
    if cv2.waitKey(1) == ord('x'):
        print("\n✅ Gesture Control Complete ✅\n")
        break