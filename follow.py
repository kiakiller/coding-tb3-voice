#!/usr/bin/python
import rospy
import cv2
import argparse
from geometry_msgs.msg import Twist
from std_msgs.msg import String
import numpy as np

cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size = 1)
rospy.init_node('jalan2_buta')

command = Twist()
command.linear.x = 0

class drive:
    def right():
        command.linear.x = 0.0
        command.angular.z = -0.5
        time.sleep(0.07)

    def left():
        command.linear.x = 0.0
        command.angular.z = 0.5
        time.sleep(0.07)

    def center1():
        command.linear.x = 0.18
        command.angular.z = 0.0
        time.sleep(0.03)

    def stop():
        command.linear.x = 0.0
        command.angular.z = 0.0
        #time.sleep(0.025)

if __name__ == "__main__":

    	camera = cv2.VideoCapture(0)
    # keep looping
    while True:
        camera.set(cv2.CAP_PROP_FPS,10)
        (grabbed, frame) = camera.read()

        #frame = imutils.resize(frame, width=600)
        # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        frame = cv2.flip(frame,1)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, Lower_range, Upper_range)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None

        # left line
        cv2.line(frame, (300 - 75 , 0), (300 - 75 , 900), (0, 255, 0), 5)
        # right line
        cv2.line(frame, (300 + 75, 0), (300 + 75, 900), (0, 255, 0), 5)
        if len(cnts)>0:
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            if x > 300 + 50 :
                detect = "LEFT"
                drive.left()

                #cv2.putText(frame, detect, (250, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2, cv2.LINE_AA)
            if x < 300 - 50:
                detect = "RIGHT"
                drive.right()

                #cv2.putText(frame, detect, (250, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2, cv2.LINE_AA)
            if x > 200 and x < 400:
                detect = "CENTER"
                drive.center1()

                #cv2.putText(frame, detect, (250, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            drive.stop()

        else:
            drive.stop()

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
camera.release()
cv2.destroyAllWindows()
