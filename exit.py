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
        if rospy.Time.now()-time_prev > rospy.Duration(8):
            state = 1
            time_prev = rospy.Time.now()
             
    elif state ==1:                                                  #foward
        command.linear.x = 0.09
        command.angular.z = -0.27
        print "foward"
        if rospy.Time.now()-time_prev > rospy.Duration(0.8):
            state = 2
            time_prev = rospy.Time.now()
            
    elif state ==2:                                                  #foward
        command.linear.x = 0.0
        command.angular.z = 0.00
        print "stop"
        if rospy.Time.now()-time_prev > rospy.Duration(0.1):
            state = 3
            time_prev = rospy.Time.now()
            
    elif state ==3:                                                  #foward
        command.linear.x = 0.09
        command.angular.z = -0.4
        print "foward"
        if rospy.Time.now()-time_prev > rospy.Duration(0.8):
            state = 4
            time_prev = rospy.Time.now()

    elif state ==4:                                                  #foward
        command.linear.x = 0.13
        command.angular.z = -0.1
        print "stop"
        if rospy.Time.now()-time_prev > rospy.Duration(0.4):
            state = 5
            time_prev = rospy.Time.now()


    elif state ==5:                                                  #left
        command.linear.x = 0.6
        command.angular.z = -0.14
        print "left"
        if rospy.Time.now()-time_prev > rospy.Duration(0.2):
            state = 6
            time_prev = rospy.Time.now()
            
    elif state ==6:                                                  #foward
        command.linear.x = 0.0
        command.angular.z = -0.2
        print "foward"
        if rospy.Time.now()-time_prev > rospy.Duration(0.8):
            state = 7
            time_prev = rospy.Time.now()
            
    elif state ==7:                                                  #foward
        command.linear.x = 0.12
        command.angular.z = -0.27
        print "foward"
        if rospy.Time.now()-time_prev > rospy.Duration(1.8):
            state = 8
            time_prev = rospy.Time.now()
            
    elif state ==8:                                                  #foward
        command.linear.x = 0.15
        command.angular.z = 0.27
        print "left"
        if rospy.Time.now()-time_prev > rospy.Duration(1.8):
            state = 9
            time_prev = rospy.Time.now()

    elif state ==9:                                                  #foward
        command.linear.x = 0.05
        command.angular.z = 0.0
        print "right"
        if rospy.Time.now()-time_prev > rospy.Duration(0.3):
            state = 10
            time_prev = rospy.Time.now()
         
    elif state ==10:                                                  #left
        command.linear.x = -0.12
        command.angular.z =0.24
        print "stop"
        if rospy.Time.now()-time_prev > rospy.Duration(0.5):
            state = 11
            time_prev = rospy.Time.now()

    elif state ==11:                                                  #left
        command.linear.x = 0.14
        command.angular.z = -0.1
        print "foward"
        if rospy.Time.now()-time_prev > rospy.Duration(1.0):
            state = 12
            time_prev = rospy.Time.now()
                                    
    elif state ==12:                                                  #left
        command.linear.x = -0.13
        command.angular.z = 0.0
        print "stop"
        if rospy.Time.now()-time_prev > rospy.Duration(0.2):
            state = 13
            time_prev = rospy.Time.now()
            
    elif state ==13:                                                  #left
        command.linear.x = 0.14
        command.angular.z = -0.3
        print "foward"
        if rospy.Time.now()-time_prev > rospy.Duration(1.0):
            state = 14
            time_prev = rospy.Time.now()
            
            
    elif state ==14:                                                  #left
        command.linear.x = 0.0
        command.angular.z = 0.0
        print "stop"
        if rospy.Time.now()-time_prev > rospy.Duration(0.1):
            state =15
            time_prev = rospy.Time.now()
            
    elif state ==15:                                                  #left
        command.linear.x = 0.15
        command.angular.z = 0.5
        print "left"
        if rospy.Time.now()-time_prev > rospy.Duration(1.05):
            state = 16
            time_prev = rospy.Time.now()
            
    elif state ==16:                                                  #left
        command.linear.x = 0.08
        command.angular.z = -0.1
        print "stop"
        if rospy.Time.now()-time_prev > rospy.Duration(0.3):
            state = 17
            time_prev = rospy.Time.now()
            
    elif state ==17:                                                  #left
        command.linear.x = 0.13
        command.angular.z = 0.2
        print "foward"
        if rospy.Time.now()-time_prev > rospy.Duration(2.0):
            state = 18
            time_prev = rospy.Time.now()
            
    elif state ==18:                                                  #left
        command.linear.x = 0.13
        command.angular.z = -0.3
        print "stop"
        if rospy.Time.now()-time_prev > rospy.Duration(1.1):
            state = 19
            time_prev = rospy.Time.now()
            
    elif state ==19:                                                  #left
        command.linear.x =0.13
        command.angular.z = 0.5
        print "foward"
        if rospy.Time.now()-time_prev > rospy.Duration(3.6):
            state = 43
            time_prev = rospy.Time.now()
 
    elif state ==23:                                                  #left
        command.linear.x =0.0
        command.angular.z = 0.0
        print "foward"
        if rospy.Time.now()-time_prev > rospy.Duration(0.3):
            state = 24
            time_prev = rospy.Time.now()
            
    elif state ==24:                                                  #left
        command.linear.x =0.13
        command.angular.z = 0.23
        print "foward"
        if rospy.Time.now()-time_prev > rospy.Duration(1.3):
            state = 25
            time_prev = rospy.Time.now()
            
    elif state ==25:                                                  #left
        command.linear.x =0.0
        command.angular.z = 0.0
        print "foward"
        if rospy.Time.now()-time_prev > rospy.Duration(1.3):
            state = 26
            time_prev = rospy.Time.now()
            
    elif state ==26:                                                  #left
        command.linear.x =0.13
        command.angular.z = 0.23
        print "foward"
        if rospy.Time.now()-time_prev > rospy.Duration(1.3):
            state = 27
            time_prev = rospy.Time.now()
            
    elif state ==27:                                                  #left
        command.linear.x =0.0
        command.angular.z = 0.0
        print "foward"
        if rospy.Time.now()-time_prev > rospy.Duration(0.3):
            state = 28
            time_prev = rospy.Time.now()
        
    elif state ==28:                                                  #left
        command.linear.x =0.13
        command.angular.z = 0.23
        print "foward"
        if rospy.Time.now()-time_prev > rospy.Duration(1.3):
            state = 29
            time_prev = rospy.Time.now()
            
    elif state ==29:                                                  #left
        command.linear.x =0.13
        command.angular.z = -0.13
        print "foward"
        if rospy.Time.now()-time_prev > rospy.Duration(0.5):
            state = 30
            time_prev = rospy.Time.now()
            
    elif state ==30:                                                  #left
        command.linear.x =0.10
        command.angular.z = 0.3
        print "foward"
        if rospy.Time.now()-time_prev > rospy.Duration(0.3):
            state = 31
            time_prev = rospy.Time.now()
            
    elif state ==31:                                                  #left
        command.linear.x =-0.10
        command.angular.z = -0.5
        print "foward"
        if rospy.Time.now()-time_prev > rospy.Duration(0.6):
            state = 32
            time_prev = rospy.Time.now()
            

    elif state ==32:                                                  #left
        command.linear.x =0.11
        command.angular.z = 0.4
        print "foward"
        if rospy.Time.now()-time_prev > rospy.Duration(0.4):
            state = 33
            time_prev = rospy.Time.now() 
            
    elif state ==33:                                                  #left
        command.linear.x =0.10
        command.angular.z = -0.23
        print "foward"
        if rospy.Time.now()-time_prev > rospy.Duration(0.2):
            state = 34
            time_prev = rospy.Time.now()
            
    elif state ==34:                                                  #left
        command.linear.x =0.12
        command.angular.z = -0.23
        print "foward"
        if rospy.Time.now()-time_prev > rospy.Duration(0.8):
            state = 35
            time_prev = rospy.Time.now()
            
    elif state ==35:                                                  #left
        command.linear.x =0.13
        command.angular.z = 0.23
        print "foward"
        if rospy.Time.now()-time_prev > rospy.Duration(1.3):
            state = 36
            time_prev = rospy.Time.now()
            
            
    elif state ==37:                                                  #left
        command.linear.x =0.13
        command.angular.z = 0.23
        print "foward"
        if rospy.Time.now()-time_prev > rospy.Duration(1.3):
            state = 38
            time_prev = rospy.Time.now()
            
            
    elif state ==39:                                                  #left
        command.linear.x =0.13
        command.angular.z = 0.23
        print "foward"
        if rospy.Time.now()-time_prev > rospy.Duration(1.3):
            state = 40
            time_prev = rospy.Time.now()
            
    elif state ==41:                                                  #left
        command.linear.x =0.13
        command.angular.z = 0.23
        print "foward"
        if rospy.Time.now()-time_prev > rospy.Duration(1.3):
            state = 42
            time_prev = rospy.Time.now()
            
    elif state ==42:                                                  #left
        command.linear.x =0.13
        command.angular.z = 0.23
        print "foward"
        if rospy.Time.now()-time_prev > rospy.Duration(1.3):
            state = 43
            time_prev = rospy.Time.now()

    elif state == 43:                                           #Stop
        command.linear.x = 0.0
        command.angular.z = 0.0
        print "stop" 
            
    # publish command 
    cmd_vel_pub.publish(command)

    rate.sleep()
    


