#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
import sys, select, os
if os.name == 'nt':
  import msvcrt
else:
  import tty, termios

from std_msgs.msg import String
import time

voice_command_ = ""

msg = """
Control Your TurtleBot3!
---------------------------
Voice command:
Stop/Forward/Backward/Left/Right

space key, s : force stop
CTRL-C to quit
"""
    
def getKey():
    if os.name == 'nt':
      return msvcrt.getch()

    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key
    
def callback(data):
    global voice_command_
        
    voice_command_ = data.data
 
if __name__=="__main__":
    if os.name != 'nt':
        settings = termios.tcgetattr(sys.stdin)

    rospy.init_node('tb3_voice')
    cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size = 1)
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    sub = rospy.Subscriber("recognizer/output", String, callback, queue_size=10)
    
    rate = rospy.Rate(10)

    state = 0   # 0 is stop, 1 is forward
    v=0
    time_prev = rospy.Time.now()

    command = Twist()
    
    while(1):
        key = getKey()
        if key == ' ' or key == 's' :
            voice_command_ = 0
        else:
            if (key == '\x03'):
                break

        os.system('cls' if os.name == 'nt' else 'clear')
        print(msg)             
          
        if voice_command_ != "":
            print(voice_command_)
    
    
        if v==0:
            
            if "speed" in voice_command_ :
                print "go to room 4" 
                if state == 0:
                    command.linear.x = 0.0
                    command.angular.z = 0.0
                    if rospy.Time.now()-time_prev > rospy.Duration(1):
                        state = 1
                        time_prev = rospy.Time.now()
                         
                elif state ==1:                                                  #foward
                    command.linear.x = 0.18
                    command.angular.z = 0.0
                    print "foward"
                    if rospy.Time.now()-time_prev > rospy.Duration(2.8):
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
                    command.linear.x = 0.18
                    command.angular.z = 0.0
                    print "foward"
                    if rospy.Time.now()-time_prev > rospy.Duration(2.0):
                        state = 4
                        time_prev = rospy.Time.now()
                     
                elif state ==4:                                                  #left
                    command.linear.x = 0.0
                    command.angular.z = -0.5
                    print "right"
                    if rospy.Time.now()-time_prev > rospy.Duration(3.1):
                        state = 5
                        time_prev = rospy.Time.now()

                elif state ==5:                                                  #left
                    command.linear.x = 0.6
                    command.angular.z = 0.0
                    print "foward"
                    if rospy.Time.now()-time_prev > rospy.Duration(4.9):
                        state = 6
                        time_prev = rospy.Time.now()
                                                
                elif state ==6:                                                  #left
                    command.linear.x = 0.0
                    command.angular.z = 0.0
                    print "stop"
                    if rospy.Time.now()-time_prev > rospy.Duration(5.05):
                        state = 7
                        time_prev = rospy.Time.now()
                        
                elif state ==7:                                                  #left
                    command.linear.x = -0.15
                    command.angular.z = 0.0
                    print "reverse"
                    if rospy.Time.now()-time_prev > rospy.Duration(2.8):
                        state = 8
                        time_prev = rospy.Time.now()
                        
                        
                elif state ==8:                                                  #left
                    command.linear.x = 0.0
                    command.angular.z = 0.5
                    print "left"
                    if rospy.Time.now()-time_prev > rospy.Duration(3.0):
                        state = 9
                        time_prev = rospy.Time.now()
                        
                elif state ==9:                                                  #left
                    command.linear.x = 0.18
                    command.angular.z = 0.0
                    print "foward"
                    if rospy.Time.now()-time_prev > rospy.Duration(4.05):
                        state = 10
                        time_prev = rospy.Time.now()
                        
                elif state ==10:                                                  #left
                    command.linear.x = 0.0
                    command.angular.z = -0.5
                    print "right"
                    if rospy.Time.now()-time_prev > rospy.Duration(3.23):
                        state = 11
                        time_prev = rospy.Time.now()
                        
                elif state ==11:                                                  #left
                    command.linear.x = 0.18
                    command.angular.z = 0.0
                    print "foward"
                    if rospy.Time.now()-time_prev > rospy.Duration(2.9):
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
                    command.linear.x =0.3
                    command.angular.z = 0.0
                    print "foward"
                    if rospy.Time.now()-time_prev > rospy.Duration(1.3):
                        state = 14
                        time_prev = rospy.Time.now()

                elif state == 14:                                           #Stop
                    command.linear.x = 0.0
                    command.angular.z = 0.0
                    print "stop"
                    v=1
                    state=0
     #   break
               
    # publish command 
        #cmd_vel_pub.publish(command)
        
            if "right" in voice_command_ :
                print "go to room 3" 
                if state == 0:
                    command.linear.x = 0.0
                    command.angular.z = 0.0
                    if rospy.Time.now()-time_prev > rospy.Duration(1):
                        state = 1
                        time_prev = rospy.Time.now()
                         
                elif state ==1:                                                  #foward
                    command.linear.x = 0.18
                    command.angular.z = 0.0
                    print "foward"
                    if rospy.Time.now()-time_prev > rospy.Duration(3.0):
                        state = 2
                        time_prev = rospy.Time.now()

                elif state ==2:                                                  #left
                    command.linear.x = 0.0
                    command.angular.z = -0.5
                    print "right"
                    if rospy.Time.now()-time_prev > rospy.Duration(3.2):
                        state = 3
                        time_prev = rospy.Time.now()

                elif state ==3:                                                  #foward
                    command.linear.x = 0.18
                    command.angular.z = 0.0
                    print "foward"
                    if rospy.Time.now()-time_prev > rospy.Duration(6.4):
                        state = 4
                        time_prev = rospy.Time.now()
                     
                elif state ==4:                                                  #left
                    command.linear.x = 0.0
                    command.angular.z = -0.5
                    print "right"
                    if rospy.Time.now()-time_prev > rospy.Duration(3.12):
                        state = 5
                        time_prev = rospy.Time.now()

                elif state ==5:                                                  #left
                    command.linear.x = 0.18
                    command.angular.z = 0.0
                    print "foward"
                    if rospy.Time.now()-time_prev > rospy.Duration(6.7):
                        state = 6
                        time_prev = rospy.Time.now()
                                                
                elif state ==6:                                                  #left
                    command.linear.x = 0.0
                    command.angular.z = -0.5
                    print "right"
                    if rospy.Time.now()-time_prev > rospy.Duration(3.1):
                        state = 7
                        time_prev = rospy.Time.now()
                        
                elif state ==7:                                                  #left
                    command.linear.x = 0.18
                    command.angular.z = 0.0
                    print "foward"
                    if rospy.Time.now()-time_prev > rospy.Duration(2.3):
                        state = 8
                        time_prev = rospy.Time.now()
                        
                        
                elif state ==8:                                                  #left
                    command.linear.x = 0.0
                    command.angular.z = 0.5
                    print "left"
                    if rospy.Time.now()-time_prev > rospy.Duration(3.1):
                        state = 9
                        time_prev = rospy.Time.now()
                        
                elif state ==9:                                                  #left
                    command.linear.x = 0.18
                    command.angular.z = 0.0
                    print "foward"
                    if rospy.Time.now()-time_prev > rospy.Duration(3.1):
                        state = 18
                        time_prev = rospy.Time.now()
                        
                elif state ==10:                                                  #left
                    command.linear.x = 0.0
                    command.angular.z = 0.0
                    print "stop"
                    if rospy.Time.now()-time_prev > rospy.Duration(5.23):
                        state = 11
                        time_prev = rospy.Time.now()
                        
                elif state ==11:                                                  #left
                    command.linear.x = -0.18
                    command.angular.z = 0.0
                    print "reverse"
                    if rospy.Time.now()-time_prev > rospy.Duration(2.9):
                        state = 12
                        time_prev = rospy.Time.now()
                        
                elif state ==12:                                                  #left
                    command.linear.x = 0.0
                    command.angular.z = 0.5
                    print "left"
                    if rospy.Time.now()-time_prev > rospy.Duration(3.12):
                        state = 13
                        time_prev = rospy.Time.now()
                        
                        
                elif state ==13:                                                  #left
                    command.linear.x =0.18
                    command.angular.z = 0.0
                    print "foward"
                    if rospy.Time.now()-time_prev > rospy.Duration(3.0):
                        state = 14
                        time_prev = rospy.Time.now()
                        
                elif state ==14:                                                  #left
                        command.linear.x =0.0
                        command.angular.z = 0.5
                        print "left"
                        if rospy.Time.now()-time_prev > rospy.Duration(3.1):
                            state = 15
                            time_prev = rospy.Time.now()
                            
                elif state ==15:                                                  #left
                        command.linear.x =0.18
                        command.angular.z = 0.0
                        print "foward"
                        if rospy.Time.now()-time_prev > rospy.Duration(3.1):
                            state = 16
                            time_prev = rospy.Time.now()
                                
                elif state ==16:                                                  #left
                            command.linear.x =0.0
                            command.angular.z = -0.5
                            print "right "
                            if rospy.Time.now()-time_prev > rospy.Duration(3.1):
                                state = 17
                                time_prev = rospy.Time.now()
                                
                elif state ==17:                                                  #left
                            command.linear.x =0.5
                            command.angular.z = -0.2
                            print "forward"
                            if rospy.Time.now()-time_prev > rospy.Duration(0.8):
                                state = 18
                                time_prev = rospy.Time.now()
                                
                elif state == 18:                                           #Stop
                    command.linear.x = 0.0
                    command.angular.z = 0.0
                    print "stop"
                    v=1
                    state=0
                    
    # publish command 
        cmd_vel_pub.publish(command)
    
        
        
        

        if v==1:
            if "halt" in voice_command_ :
                print "go to room 1" 
                if state == 0:
                    command.linear.x = 0.0
                    command.angular.z = 0.0
                    if rospy.Time.now()-time_prev > rospy.Duration(1):
                        state = 1
                        time_prev = rospy.Time.now()
                        
                elif state ==1:                                                  #left
                    command.linear.x = -0.18
                    command.angular.z = 0.0
                    print "reverse"
                    if rospy.Time.now()-time_prev > rospy.Duration(3.1):
                        state = 2
                        time_prev = rospy.Time.now()
                        
                elif state ==2:                                                  #left
                    command.linear.x = 0.0
                    command.angular.z = 0.5
                    print "left"
                    if rospy.Time.now()-time_prev > rospy.Duration(3.12):
                        state = 3
                        time_prev = rospy.Time.now()
                        
                        
                elif state ==3:                                                  #left
                    command.linear.x =0.18
                    command.angular.z = 0.0
                    print "foward"
                    if rospy.Time.now()-time_prev > rospy.Duration(2.3):
                        state = 4
                        time_prev = rospy.Time.now()
                        
                elif state ==4:                                                  #left
                        command.linear.x =0.0
                        command.angular.z = 0.5
                        print "left"
                        if rospy.Time.now()-time_prev > rospy.Duration(3.1):
                            state = 5
                            time_prev = rospy.Time.now()
                            
                elif state ==5:                                                  #left
                        command.linear.x =0.18
                        command.angular.z = 0.0
                        print "foward"
                        if rospy.Time.now()-time_prev > rospy.Duration(1.1):
                            state = 6
                            time_prev = rospy.Time.now()
                                
                elif state ==6:                                                  #left
                            command.linear.x =0.0
                            command.angular.z = -0.5
                            print "right "
                            if rospy.Time.now()-time_prev > rospy.Duration(3.1):
                                state = 7
                                time_prev = rospy.Time.now()
                                
                elif state ==7:                                                  #left
                            command.linear.x =0.5
                            command.angular.z = -0.2
                            print "forward"
                            if rospy.Time.now()-time_prev > rospy.Duration(0.8):
                                state = 8
                                time_prev = rospy.Time.now()

                elif state ==8:                                                  #foward
                    command.linear.x = 0.19
                    command.angular.z = -0.01
                    print "foward"
                    if rospy.Time.now()-time_prev > rospy.Duration(4.4):
                        state = 9
                        time_prev = rospy.Time.now()

                elif state ==9:                                                  #left
                    command.linear.x = 0.0
                    command.angular.z = 0.5
                    print "left"
                    if rospy.Time.now()-time_prev > rospy.Duration(3.3):
                        state = 10
                        time_prev = rospy.Time.now()

                elif state ==10:                                                  #foward
                    command.linear.x = 0.18
                    command.angular.z = 0.0
                    print "foward"
                    if rospy.Time.now()-time_prev > rospy.Duration(3.4):
                        state = 15
                        time_prev = rospy.Time.now()
                     
                elif state ==11:                                                  #left
                    command.linear.x = 0.0
                    command.angular.z = 0.5
                    print "left"
                    if rospy.Time.now()-time_prev > rospy.Duration(3.1):
                        state = 12
                        time_prev = rospy.Time.now()

                elif state ==12:                                                  #left
                    command.linear.x = 0.18
                    command.angular.z = 0.0
                    print "foward"
                    if rospy.Time.now()-time_prev > rospy.Duration(0.9):
                        state = 13
                        time_prev = rospy.Time.now()
                                                
                elif state ==13:                                                  #left
                    command.linear.x = 0.0
                    command.angular.z = -0.5
                    print "right"
                    if rospy.Time.now()-time_prev > rospy.Duration(3.1):
                        state = 14
                        time_prev = rospy.Time.now()
                        
                elif state ==14:                                                  #left
                    command.linear.x = 0.18
                    command.angular.z = 0.0
                    print "foward"
                    if rospy.Time.now()-time_prev > rospy.Duration(2.7):
                        state = 15
                        time_prev = rospy.Time.now()
                        
                        
                elif state ==15:                                                  #left
                    command.linear.x = 0.0
                    command.angular.z = 0.0
                    print "stop"


            
                    
            if"back" in voice_command_ :
                print "go to room 2"
                if state == 0:
                    command.linear.x = 0.0
                    command.angular.z = 0.0
                    if rospy.Time.now()-time_prev > rospy.Duration(1):
                        state = 1
                        time_prev = rospy.Time.now()
                        
                elif state ==1:                                                  #left
                    command.linear.x = -0.18
                    command.angular.z = 0.0
                    print "reverse"
                    if rospy.Time.now()-time_prev > rospy.Duration(3.1):
                        state = 2
                        time_prev = rospy.Time.now()
                        
                elif state ==2:                                                  #left
                    command.linear.x = 0.0
                    command.angular.z = 0.5
                    print "left"
                    if rospy.Time.now()-time_prev > rospy.Duration(3.12):
                        state = 3
                        time_prev = rospy.Time.now()
                        
                        
                elif state ==3:                                                  #left
                    command.linear.x =0.18
                    command.angular.z = 0.0
                    print "foward"
                    if rospy.Time.now()-time_prev > rospy.Duration(2.3):
                        state = 4
                        time_prev = rospy.Time.now()
                        
                elif state ==4:                                                  #left
                        command.linear.x =0.0
                        command.angular.z = 0.5
                        print "left"
                        if rospy.Time.now()-time_prev > rospy.Duration(3.25):
                            state = 5
                            time_prev = rospy.Time.now()
                            
                elif state ==5:                                                  #left
                        command.linear.x =0.18
                        command.angular.z = 0.0
                        print "foward"
                        if rospy.Time.now()-time_prev > rospy.Duration(1.1):
                            state = 6
                            time_prev = rospy.Time.now()
                                
                elif state ==6:                                                  #left
                            command.linear.x =0.0
                            command.angular.z = -0.5
                            print "right "
                            if rospy.Time.now()-time_prev > rospy.Duration(3.1):
                                state = 7
                                time_prev = rospy.Time.now()
                                
                elif state ==7:                                                  #left
                            command.linear.x =0.5
                            command.angular.z = -0.2
                            print "forward"
                            if rospy.Time.now()-time_prev > rospy.Duration(0.8):
                                state = 8
                                time_prev = rospy.Time.now()
                         
                elif state ==8:                                                  #foward
                    command.linear.x = 0.2
                    command.angular.z = -0.02
                    print "foward"
                    if rospy.Time.now()-time_prev > rospy.Duration(4.0):
                        state = 9
                        time_prev = rospy.Time.now()

                elif state ==9:                                                  #left
                    command.linear.x = 0.0
                    command.angular.z = -0.5
                    print "right"
                    if rospy.Time.now()-time_prev > rospy.Duration(3.3):
                        state = 10
                        time_prev = rospy.Time.now()

                elif state ==10:                                                  #foward
                    command.linear.x = 1.0
                    command.angular.z = 0.0
                    print "foward"
                    if rospy.Time.now()-time_prev > rospy.Duration(3.3):
                        state = 15
                        time_prev = rospy.Time.now()
                     
                elif state ==11:                                                  #left
                    command.linear.x = 0.01
                    command.angular.z = -0.5
                    print "right"
                    if rospy.Time.now()-time_prev > rospy.Duration(3.2):
                        state = 12
                        time_prev = rospy.Time.now()

                elif state ==12:                                                  #left
                    command.linear.x = 0.18
                    command.angular.z = 0.01
                    print "foward"
                    if rospy.Time.now()-time_prev > rospy.Duration(3.3):
                        state = 13
                        time_prev = rospy.Time.now()
                                                
                elif state ==13:                                                  #left
                    command.linear.x = 0.0
                    command.angular.z =0.5
                    print "left"
                    if rospy.Time.now()-time_prev > rospy.Duration(3.15):
                        state = 14
                        time_prev = rospy.Time.now()
                        
                elif state ==14:                                                  #left
                    command.linear.x = 0.18
                    command.angular.z = 0.0
                    print "foward"
                    if rospy.Time.now()-time_prev > rospy.Duration(1.5):
                        state = 15
                        time_prev = rospy.Time.now()
                        
                        
                elif state ==15:                                                 #left
                    command.linear.x = 0.0
                    command.angular.z = 0.0
                    print "stop"

            # publish command 
       # cmd_vel_pub.publish(command)
                    


            
        
        

       # pass
        #voice_command_=""
        #elif "left" in voice_command_ :
            #twist.linear.x =  0.0
            #twist.angular.z = 1.0
        #elif "right" in voice_command_ :
            #twist.linear.x =   0.0
            #twist.angular.z = -1.0
        #else:
            #twist.linear.x =  0.0
            #twist.angular.z = 0.0
          
            #cmd_vel_pub.publish(command)
 
            #print("cmd_vel: linear.x: %.3f, angular.z: %.3f" % (command.linear.x, command.angular.z))        
        #pub.publish(twist)
       # if command.linear.x != 0.0 or command.angular.z != 0.0:
            #start_time = time.time()
               #while rospy.Time.now()-time_prev > rospy.Duration(0.0):
               #pass
               #voice_command_ = ""     

    if os.name != 'nt':
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
