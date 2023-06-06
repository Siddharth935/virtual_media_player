import cv2
import pyautogui as p
import HandTrackingModule as htm
import time

wSrn, hSrn = 640, 480
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, wSrn)
cap.set(4, hSrn)
pTime = 0
tipIds = [4, 8, 12, 16, 20]

detecor = htm.handDetector(maxHands=2, detectionCon=0.5)


while True:
    success, img = cap.read()
    img = detecor.findHands(img)
    lmList = detecor.findPosition(img, draw=False)

    if len(lmList) != 0:
        x0, y0 = lmList[4][1], lmList[4][2]
        x1, y1 = lmList[8][1], lmList[8][2]

        fingers = []
        # Thumb
        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        # four finger
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        # print(fingers)
        totalFinger = fingers.count(1)
        print(totalFinger)


        if totalFinger == 5:
            cv2.circle(img, (x1, y1), 15, (0, 0, 255), cv2.FILLED)
            p.press("space")
        elif totalFinger == 4:
            p.press("right")
        elif totalFinger == 3:
            p.press("left")
        elif totalFinger == 2:
            p.press("volumeup")
        elif totalFinger == 1:
            p.press("volumedown")

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (30, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)

    cv2.imshow("Video", img)
    k = cv2.waitKey(1)
    if k == ord('q'):
        break

cv2.destroyAllWindows()