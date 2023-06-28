import cv2
import numpy as np
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

minPixelv = 40 #can set as per need
maxPixelv = 230 #can set as per need

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
minVol = volume.GetVolumeRange()[0]
maxVol = volume.GetVolumeRange()[1]

def GVCfunc(frame,xt,yt,xr,yr,lmList):
    if len(lmList)!=0:
        cxv, cyv = (xt+xr)//2, (yt+yr)//2
        netlengthv = math.hypot(xr-xt,yr-yt)

        newvol = np.interp(netlengthv, [minPixelv,maxPixelv], [minVol,maxVol])
        newvolbar = np.interp(netlengthv, [minPixelv,maxPixelv], [380,100])
        newvolper = np.interp(netlengthv, [minPixelv,maxPixelv], [0,100])
        volume.SetMasterVolumeLevel(newvol, None)

        cv2.circle(frame, (xt,yt), 10, (200,0,0), -1)
        cv2.circle(frame, (xr,yr), 10, (200,0,0), -1)
        cv2.circle(frame, (cxv,cyv), 10, (200,0,0), -1)
        cv2.line(frame, (xt,yt), (xr,yr), (200,0,0), 3)

        if netlengthv<minPixelv:
            cv2.circle(frame, (cxv,cyv), 10, (0,255,0), -1)
            cv2.putText(frame,"Muted",(36,90),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255, 0),2)

        if netlengthv>maxPixelv:
            cv2.circle(frame, (xt,yt), 10, (0,255,0), -1)
            cv2.circle(frame, (xr,yr), 10, (0,255,0), -1)
            cv2.putText(frame,"MaxVol",(33,90),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255, 0),2)

        cv2.rectangle(frame, (40,100), (75,380), (200,0,0), 3)
        cv2.rectangle(frame, (40, int(newvolbar)), (75,380), (200,0,0), -1)
        cv2.putText(frame,str(int(newvolper))+" %",(39,407),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 0, 0),2)
