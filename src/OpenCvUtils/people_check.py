import cv2
import numpy as np
from imutils.object_detection import non_max_suppression
import imutils

def main():
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    cap = cv2.VideoCapture("E:/AI/chache/堆高機輔助警報系統動態測試.mp4")

    while True:
        ret, image = cap.read()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        people, b = hog.detectMultiScale(gray,
                                  winStride = (4, 4),
                                  padding = (4, 4),
                                  scale = 1.29,
                                  useMeanshiftGrouping = False)
        for x, y, w, h in people:
            cv2.rectangle(image, (x, y), (x+w, y+h), (0,255,0), 2)
            cv2.putText(image, 'people', (x, y-5), 1, 1, (0,0,255),1)

        reImage = cv2.resize(image, (800, 420))
        cv2.imshow("yukicv", reImage)
        if cv2.waitKey(1) & 0xff == 27:
            cv2.destroyAllWindows()
            break

if __name__ == '__main__':
    main()
