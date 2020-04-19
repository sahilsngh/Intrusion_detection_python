import cv2
import numpy as np
import pandas as pd

a = 0
q = int(input('Enter your camera port:\n 1: for external port \n 2: for internal camera.\n Input:  '))
first_frame = None
#Create a file or video recording file. Note - provide your own directory.
filename = "sample_camera/file_%a.avi" % a
video = cv2.VideoCapture(q)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(filename, fourcc, 25.0, (640, 480))

while True:
    check, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if first_frame is None:
        first_frame = gray
        continue

    # cv2.imshow('First', first_frame)
    # cv2.imshow('gray', gray)
    delta_frame = cv2.absdiff(first_frame, gray)
    thresh_delta = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    thresh_delta = cv2.dilate(thresh_delta, None, iterations=0)

    # Use this code when you know the open cv version.
    # ret, cnts, hierarchy = cv2.findContours(thresh_delta.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # or use code below |
    # This provides you a code that could run on last or older version of OpenCV.
    major = cv2.__version__.split('.')[0]
    if major == '3':
        ret, cnts, hierarchy = cv2.findContours(thresh_delta.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    else:
        cnts, hierarchy = cv2.findContours(thresh_delta.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) < 1000:
            continue
        else:
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
            a += 1
            out.write(frame)


    cv2.imshow("capturing", gray)
    cv2.imshow("delta_frame", delta_frame)
    cv2.imshow("thresh_frame", thresh_delta)
    cv2.imshow("frame", frame)
    cv2.resizeWindow('capturing', 500, 500)
    cv2.resizeWindow('delta_frame', 500, 500)
    cv2.resizeWindow('thresh_frame', 500, 500)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
print(a)
out.release()
video.release()
cv2.destroyAllWindows()
