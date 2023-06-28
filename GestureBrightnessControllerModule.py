import cv2
import numpy as np
import math
import screen_brightness_control as sbc

minPixelb = 30 #can set as per need
maxPixelb = 250 #can set as per need

def GVBfunc(frame,xt,yt,xm,ym,lmList):
    if len(lmList)!=0:
        cxb, cyb = (xt+xm)//2, (yt+ym)//2
        netlengthb = math.hypot(xm-xt,ym-yt)

        newbright = np.interp(netlengthb, [minPixelb,maxPixelb], [0,100])
        newbrightbar = np.interp(netlengthb, [minPixelb,maxPixelb], [380,100])
        newbrightper = np.interp(netlengthb, [minPixelb,maxPixelb], [0,100])
        sbc.set_brightness(newbright)

        cv2.circle(frame, (xt,yt), 10, (200,0,0), -1)
        cv2.circle(frame, (xm,ym), 10, (200,0,0), -1)
        cv2.circle(frame, (cxb,cyb), 10, (200,0,0), -1)
        cv2.line(frame, (xt,yt), (xm,ym), (200,0,0), 3)

        if netlengthb<minPixelb:
            cv2.circle(frame, (cxb,cyb), 10, (0,255,0), -1)
            cv2.putText(frame,"Dimmed",(27,90),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255, 0),2)

        if netlengthb>maxPixelb:
            cv2.circle(frame, (xt,yt), 10, (0,255,0), -1)
            cv2.circle(frame, (xm,ym), 10, (0,255,0), -1)
            cv2.putText(frame,"MaxBright",(19,90),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255, 0),2)

        cv2.rectangle(frame, (40,100), (75,380), (200,0,0), 3)
        cv2.rectangle(frame, (40, int(newbrightbar)), (75,380), (200,0,0), -1)
        cv2.putText(frame,str(int(newbrightper))+" %",(39,407),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 0, 0),2)
