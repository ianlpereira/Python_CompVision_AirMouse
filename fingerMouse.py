import cv2
import time
import os
import handTrackingModule as htm
import win32con, win32api

wCam, hCam = 2560, 1080

cap = cv2.VideoCapture(1)
# cap.set()
cap.set(3, wCam)
cap.set(4, hCam)

folderPath = "FingerPics"
myList = os.listdir(folderPath)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)

pTime = 0
print(len(overlayList))

detector = htm.handDetector(detectionCon=0.75)

tipIds = [4, 8, 12, 16, 20]

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        fingers = []

        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        if fingers[1] == 1:
            curPosX, curPosY = lmList[7][1] * 1.5, lmList[7][2] * 1.5
            curPosX = 2560 - curPosX
            win32api.SetCursorPos((int(curPosX), int(curPosY)))
        if fingers == [0, 0, 0, 0, 0]:
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
            time.sleep(1)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
            print('Left Click')
        # print(fingers)
        totalFingers = fingers.count(1)
        # print(totalFingers)

        h, w, c = overlayList[totalFingers].shape
        img[0:h, 0:w] = overlayList[totalFingers]
        cv2.putText(img, f'Dedos Levantados: {int(totalFingers)}', (0, 500), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255),
                    3)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
