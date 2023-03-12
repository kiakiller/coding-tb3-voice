#!/usr/bin/env python

import rospy
import cv2
import argparse
from geometry_msgs.msg import Twist
from std_msgs.msg import String
import numpy as np


def nothing(x):
    pass
cv2.namedWindow("Lines", 0)
cv2.createTrackbar('Right','Lines',200,320,nothing)
cv2.createTrackbar('Left','Lines',100,320,nothing)
cv2.createTrackbar('Goal','Lines',420,480,nothing)
cv2.createTrackbar('Cnts','Lines',0,50,nothing)

def callback(value):
    pass


def setup_trackbars(range_filter):
    cv2.namedWindow("Trackbars", 0)

    for i in ["MIN", "MAX"]:
        v = 0 if i == "MIN" else 255

        for j in range_filter:
            cv2.createTrackbar("%s_%s" % (j, i), "Trackbars", v, 255, callback)


def get_arguments():
    ap = argparse.ArgumentParser()
    ap.add_argument('-f', '--filter', required=True,
                    help='Range filter. RGB or HSV')
    ap.add_argument('-w', '--webcam', required=False,
                    help='Use webcam', action='store_true')
    args = vars(ap.parse_args())

    if not args['filter'].upper() in ['RGB', 'HSV']:
        ap.error("Please speciy a correct filter.")

    return args


def get_trackbar_values(range_filter):
    values = []

    for i in ["MIN", "MAX"]:
        for j in range_filter:
            v = cv2.getTrackbarPos("%s_%s" % (j, i), "Trackbars")
            values.append(v)
    return values

#Create note for movement
cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size = 1) # to move the robot
#scan_sub = rospy.Subscriber('scan', LaserScan, scan_callback)   # to read the laser scanner
rospy.init_node('score_goal')

command = Twist()

def main():
    args = get_arguments()

    range_filter = args['filter'].upper()

    camera = cv2.VideoCapture(0)

    setup_trackbars(range_filter)

    goal = False
    
    while (True):#(goal==False):
        if args['webcam']:
            ret, image = camera.read()

            if not ret:
                break

            if range_filter == 'RGB':
                frame_to_thresh = image.copy()
            else:
                frame_to_thresh = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        v1_min, v2_min, v3_min, v1_max, v2_max, v3_max = get_trackbar_values(range_filter)

#INPUT COLOR VALUE HERE
        # get current positions of four trackbars
        L_line = cv2.getTrackbarPos('Left','Lines')
        R_L = cv2.getTrackbarPos('Right','Lines')
        R_line = R_L + 320 
        X_line = cv2.getTrackbarPos('Goal','Lines')
        Goal_cnts = cv2.getTrackbarPos('Cnts','Lines')

        cv2.line(image,(L_line,0),(L_line,480),(0,255,0),5) #Left line
        cv2.line(image,(R_line,0),(R_line,480),(0,255,0),5) #Right Line
        cv2.line(image,(0,X_line),(640,X_line),(0,0,255),5) #Forward Line

        #thresh = cv2.inRange(frame_to_thresh, (v1_min, v2_min, v3_min), (v1_max, v2_max, v3_max))

        #BALL COLOR        
        thresh = cv2.inRange(frame_to_thresh, (21, 82, 162), (79, 255, 255))

        kernel = np.ones((5,5),np.uint8)
        mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
 
        # only proceed if at least one contour was found
        if len(cnts)==0:
            cv2.putText(image,"FIND BALL", (180,90), cv2.FONT_HERSHEY_SIMPLEX, 2,(0, 0, 255),4)
            command.linear.x =  0.0
            command.angular.z = 0.5 # turn around to find ball
            cmd_vel_pub.publish(command)

        elif len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
 

#PUT ALL OTHER CODES UNDER HERE
            

           # cv2.line(image,(210,0),(210,480),(0,255,0),5) #Left line
          #  cv2.line(image,(430,0),(430,480),(0,255,0),5) #Right Line
           # cv2.line(image,(430,0),(430,480),(0,255,0),5) #Right Line

            # only proceed if the radius meets a minimum size
            if radius > 10:
                # draw the circle and centre on the frame,
                # then update the list of tracked points
                cv2.circle(image, (int(x), int(y)), int(radius),(0, 255, 255), 2)
                cv2.circle(image, center, 3, (0, 0, 255), -1)
                cv2.putText(image,"centre", (center[0]+10,center[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(0, 0, 255),1)
                cv2.putText(image,"("+str(center[0])+","+str(center[1])+")", (center[0]+10,center[1]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(0, 0, 255),1)
 

# DIRECTION CODE

            if center[0] < L_line:                
                cv2.putText(image,"LEFTB", (250,60), cv2.FONT_HERSHEY_SIMPLEX, 2,(0, 0, 255),5)
                goal = False
                command.linear.x =  0.2
                command.angular.z = 0.5 # turn left to find ball
                cmd_vel_pub.publish(command)
            elif center[0] > R_line:
                cv2.putText(image,"RIGHTB", (250,60), cv2.FONT_HERSHEY_SIMPLEX, 2,(0, 0, 255),5)
                goal = False
                command.linear.x =  0.2
                command.angular.z = -0.5 # turn right to find ball
                cmd_vel_pub.publish(command)
            #FIND GOAL WHEN BALL NEAR ROBOT
            elif center[1] >420:
                cv2.putText(image,"FIND GOAL", (180,90), cv2.FONT_HERSHEY_SIMPLEX, 2,(255, 0, 0),4)
                goal = True

        #FINDING GOAL
                         
                #while (goal==True):             
                if args['webcam']:
                    ret, image = camera.read()

                    if not ret:
                        break

                    if range_filter == 'RGB':
                        frame_to_thresh1 = image.copy()
                    else:
                        frame_to_thresh1 = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
                v1_min, v2_min, v3_min, v1_max, v2_max, v3_max = get_trackbar_values(range_filter)

                cv2.line(image,(L_line,0),(L_line,480),(0,255,0),5) #Left line
                cv2.line(image,(R_line,0),(R_line,480),(0,255,0),5) #Right Line
                cv2.line(image,(0,X_line),(640,X_line),(0,0,255),5) #Forward Line
            #INPUT COLOR VALUE HERE
                           
                #thresh1 = cv2.inRange(frame_to_thresh1, (v1_min, v2_min, v3_min), (v1_max, v2_max, v3_max))

            #GOAL COLOR
                thresh1 = cv2.inRange(frame_to_thresh1, (89, 74, 0), (114, 255, 255))

                kernel = np.ones((5,5),np.uint8) 
                mask = cv2.morphologyEx(thresh1, cv2.MORPH_OPEN, kernel)
                mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

            # find contours in the mask and initialize the current
            # (x, y) center1 of the ball
                cnts1 = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
                center1 = None
 
               # Rotate robot to find goal
                #if len(cnts1) < Goal_cnts:
                #   cv2.putText(image,"FIND GOAL 1", (180,90), cv2.FONT_HERSHEY_SIMPLEX, 2,(255, 0, 255),4)                    
              # only proceed if at least one contour was found           
                if len(cnts1) > 0:
              # find the largest contour in the mask, then use
              # it to compute the minimum enclosing circle and
              # centroid
                    c = max(cnts1, key=cv2.contourArea)
                    ((x, y), radius1) = cv2.minEnclosingCircle(c)
                    M = cv2.moments(c)
                    center1 = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                    #cv2.putText(image,"("+str(cnts1)+")", (40,200), cv2.FONT_HERSHEY_SIMPLEX, 1,(255, 0, 255),2)    

        #PUT ALL OTHER CODES UNDER HERE
            

               # cv2.line(image,(210,0),(210,480),(0,255,0),5) #Left lineex
              #  cv2.line(image,(430,0),(430,480),(0,255,0),5) #Right Line
               # cv2.line(image,(430,0),(430,480),(0,255,0),5) #Right Line

               # Rotate robot to find goal  if the radius does not meets a minimum size
                    if radius1 <20:
                        cv2.putText(image,"FIND GOAL 1", (180,100), cv2.FONT_HERSHEY_SIMPLEX, 2,(255, 0, 255),4)
                        command.linear.x =  0.0
                        command.angular.z = 0.5 # turn around to find ball
                        cmd_vel_pub.publish(command)

              # only proceed if the radius meets a minimum size                       
                    elif radius1 > 20:
                    # draw the circle and centre on the frame,
                   # then update the list of tracked points
                        cv2.circle(image, (int(x), int(y)), int(radius1),(255, 255, 255), 2)
                        cv2.circle(image, center1, 3, (0, 0, 255), -1)
                        cv2.putText(image,"centre", (center1[0]+10,center1[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(255, 0, 255),1)
                        cv2.putText(image,"("+str(center1[0])+","+str(center1[1])+")", (center1[0]+10,center1[1]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(255, 0, 255),1)
 
    
            # DIRECTION CODE TO GOAL
                    if center1[0] < L_line:                
                        cv2.putText(image,"LEFTG", (250,60), cv2.FONT_HERSHEY_SIMPLEX, 2,(255, 0, 255),5)
                        command.linear.x =  0.2
                        command.angular.z = 0.5 # turn left
                        cmd_vel_pub.publish(command)
    
                    elif center1[0] > R_line:
                        cv2.putText(image,"RIGHTG", (250,60), cv2.FONT_HERSHEY_SIMPLEX, 2,(255, 0, 255),5)
                        command.linear.x =  0.2
                        command.angular.z = -0.5 # turn right
                        cmd_vel_pub.publish(command)


                    elif center1[0] < R_line:
                        cv2.putText(image,"FORWARDG", (180,90), cv2.FONT_HERSHEY_SIMPLEX, 2,(255, 0, 255),4)
                        command.linear.x =  0.6
                        command.angular.z = 0.0 # go foward
                        cmd_vel_pub.publish(command)
                              
                    #else:
                        #goal = False
                        #cv2.putText(image,"FINDGOAL", (210,60), cv2.FONT_HERSHEY_SIMPLEX, 2,(0, 0, 255),5)
                    

             #show the frame to our screen
                    #cv2.imshow("Original", image)
                    #cv2.imshow("Thresh", thresh1)
                    #cv2.imshow("Mask", mask)

                #if cv2.waitKey(1) & 0xFF is ord('q'):
                #    break
                #goal = False


            else:
                cv2.putText(image,"FOWARDB", (210,60), cv2.FONT_HERSHEY_SIMPLEX, 2,(0, 0, 255),5)
                goal = False
                command.linear.x =  0.5
                command.angular.z = 0.0 # Go to ball
                cmd_vel_pub.publish(command)

              
        # show the frame to our screen
        cv2.imshow("Original", image)
        cv2.imshow("Thresh", thresh)
        cv2.imshow("Mask", mask)

        if cv2.waitKey(1) & 0xFF is ord('q'):
            command.linear.x =  0.0
            command.angular.z = 0.0 # STOP ROBOT
            cmd_vel_pub.publish(command)
            break


if __name__ == '__main__':
    main()
