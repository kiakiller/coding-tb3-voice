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
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    sub = rospy.Subscriber("recognizer/output", String, callback, queue_size=10)

    twist = Twist()
    
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

        if "forward" in voice_command_ :
            twist.linear.x =  0.1
            twist.angular.z = 0.0
        elif "back" in voice_command_ :
            twist.linear.x = -0.1
            twist.angular.z = 0.0
        elif "left" in voice_command_ :
            twist.linear.x =  0.0
            twist.angular.z = 1.0
        elif "right" in voice_command_ :
            twist.linear.x =   0.0
            twist.angular.z = -1.0
        else:
            twist.linear.x =  0.0
            twist.angular.z = 0.0
 
        print("cmd_vel: linear.x: %.3f, angular.z: %.3f" % (twist.linear.x, twist.angular.z))        
        pub.publish(twist)
        if twist.linear.x != 0.0 or twist.angular.z != 0.0:
            start_time = time.time()
            while time.time()-start_time < 1.0 :
                pass
            voice_command_ = ""     

    if os.name != 'nt':
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)