#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist

cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size = 1)
rospy.init_node('jalan2_buta')

command = Twist()
command.linear.x = 0
	
rate = rospy.Rate(10)

state = 0   # 0 is stop, 1 is forward
time_prev = rospy.Time.now()

while not rospy.is_shutdown():
    # check state
    #if state == 0:
     #   command.linear.x = 0
      #  if rospy.Time.now()-time_prev > rospy.Duration(10):
       #     state = 1
        #    time_prev = rospy.Time.now() 
   # elif state == 1:
    #    command.linear.x = 0.1
     #   if rospy.Time.now()-time_prev > rospy.Duration(10):
      #      state = 0
       #     time_prev = rospy.Time.now() 
    if state == 0:
        command.linear.x = 0.0
        command.angular.z = 0.0
        if rospy.Time.now()-time_prev > rospy.Duration(1):
            state = 1
            time_prev = rospy.Time.now()
             
    elif state ==1:                                                  #foward
        command.linear.x = 0.2
        command.angular.z = -0.02
        print "foward"
        if rospy.Time.now()-time_prev > rospy.Duration(4.2):
            state = 2
            time_prev = rospy.Time.now()

    elif state ==2:                                                  #left
        command.linear.x = 0.0
        command.angular.z = -0.5
        print "right"
        if rospy.Time.now()-time_prev > rospy.Duration(3.1):
            state = 3
            time_prev = rospy.Time.now()

    elif state ==3:                                                  #foward
        command.linear.x = 1.0
        command.angular.z = 0.0
        print "foward"
        if rospy.Time.now()-time_prev > rospy.Duration(1.8):
            state = 4
            time_prev = rospy.Time.now()
         
    elif state ==4:                                                  #left
        command.linear.x = 0.01
        command.angular.z = -0.5
        print "right"
        if rospy.Time.now()-time_prev > rospy.Duration(3.2):
            state = 5
            time_prev = rospy.Time.now()

    elif state ==5:                                                  #left
        command.linear.x = 0.18
        command.angular.z = 0.01
        print "foward"
        if rospy.Time.now()-time_prev > rospy.Duration(3.9):
            state = 6
            time_prev = rospy.Time.now()
                                    
    elif state ==6:                                                  #left
        command.linear.x = 0.0
        command.angular.z =0.5
        print "left"
        if rospy.Time.now()-time_prev > rospy.Duration(3.25):
            state = 7
            time_prev = rospy.Time.now()
            
    elif state ==7:                                                  #left
        command.linear.x = 0.18
        command.angular.z = 0.0
        print "foward"
        if rospy.Time.now()-time_prev > rospy.Duration(1.2):
            state = 8
            time_prev = rospy.Time.now()
            
            
    elif state ==8:                                                 #left
        command.linear.x = 0.0
        command.angular.z = 0.0
        print "stop"
        if rospy.Time.now()-time_prev > rospy.Duration(5.0):
            state = 9
            time_prev = rospy.Time.now()
            
    elif state ==9:                                                  #left
        command.linear.x = -0.15
        command.angular.z = 0.0
        print "reverse"
        if rospy.Time.now()-time_prev > rospy.Duration(2.0):
            state = 10
            time_prev = rospy.Time.now()
            
    elif state ==10:                                                  #left
        command.linear.x = 0.0
        command.angular.z = 0.5
        print "left"
        if rospy.Time.now()-time_prev > rospy.Duration(3.2):
            state = 11
            time_prev = rospy.Time.now()
            
    elif state ==11:                                                  #left
        command.linear.x = 0.18
        command.angular.z = 0.0
        print "foward"
        if rospy.Time.now()-time_prev > rospy.Duration(3.9):
            state = 12
            time_prev = rospy.Time.now()
            
    elif state ==12:                                                  #left
        command.linear.x = 0.0
        command.angular.z = 0.5
        print "left"
        if rospy.Time.now()-time_prev > rospy.Duration(3.1):
            state = 13
            time_prev = rospy.Time.now()
            
    elif state ==13:                                                  #left
        command.linear.x =0.18
        command.angular.z = 0.0
        print "foward"
        if rospy.Time.now()-time_prev > rospy.Duration(1.0):
            state = 14
            time_prev = rospy.Time.now()
            
    elif state ==14:                                                  #left
            command.linear.x = 0.01
            command.angular.z = 0.5
            print "left"
            if rospy.Time.now()-time_prev > rospy.Duration(3.25):
                state = 15
                time_prev = rospy.Time.now()
                
    elif state ==15:                                                  #left
            command.linear.x =0.18
            command.angular.z = 0.01
            print "foward"
            if rospy.Time.now()-time_prev > rospy.Duration(4.2):
                state = 16
                time_prev = rospy.Time.now()                

    elif state == 16:                                           #Stop
        command.linear.x = 0.0
        command.angular.z = 0.0
        print "stop" 
            
    # publish command 
    cmd_vel_pub.publish(command)

    rate.sleep()
    

