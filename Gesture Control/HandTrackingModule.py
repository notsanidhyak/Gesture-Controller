import cv2
import mediapipe as mp
import time

class HandDetector():

    def __init__(self):
        self.mpht = mp.solutions.hands
        self.handobj = self.mpht.Hands()
        self.mpdd = mp.solutions.drawing_utils

    def findHands(self, frame, draw=True):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.handobj.process(rgb_frame)
        if self.results.multi_hand_landmarks:
            for i in self.results.multi_hand_landmarks:
                if draw:
                    self.mpdd.draw_landmarks(frame, i, self.mpht.HAND_CONNECTIONS)
        return frame

    def findLoc(self, frame, handNo=0, draw=True):
        lmList=[]
        if self.results.multi_hand_landmarks:
            handAsked = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(handAsked.landmark):
                h,w,c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(frame, (cx,cy), 6, (190,0,0), -1)
        return lmList   

def main():
    prevtime = 0
    vidcap = cv2.VideoCapture(0)
    detectorobj = HandDetector()
    while True:
        ret, frameflip = vidcap.read()
        frame = cv2.flip(frameflip,1)
        frame = detectorobj.findHands(frame)
        lmList = detectorobj.findLoc(frame, 0, False)
        lmNo = 8 #set landmark no here to print
        if len(lmList)!=0:
            print(lmList[lmNo]) 
        
        currtime = time.time()
        fps = 1/(currtime-prevtime)
        prevtime = currtime
        cv2.putText(frame,str(int(fps))+" FPS",(10,20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 200),2)

        cv2.imshow('Realtime Hand Detector', frame)
        if cv2.waitKey(1) == ord('x'):
            break   

if __name__ == "__main__":
    main()
