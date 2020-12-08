import numpy as np
import cv2

cap = cv2.VideoCapture("rtsp://admin:wlgcbkq1234@172.31.50.222:554/h264/ch1/main/av_stream")

while (cap.isOpened()):
    ret, frame = cap.read()
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()