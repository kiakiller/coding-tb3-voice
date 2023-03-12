#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
import sys, select, os
if os.name == 'nt':
  import msvcrt
else:
  import tty, termios
  
from opencv_apps.msg import RotatedRectStamped

object_x_ = -1

msg = """
Control Your TurtleBot3!
---------------------------
Moving around:
   q    w
   a    s    d
        x
q : turn with camshift
w/x : forward/backward
a/d : turn left/right
space key, s : force stop
CTRL-C to quit
"""

def getKey():
    if os.name == 'nt':
      if sys.version_info[0] >= 3:
        return msvcrt.getch().decode()
      else:
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
    global object_x_
    
    if data.rect.center.x > -1 and data.rect.center.x < 640 :
        object_x_ = data.rect.center.x 

if __name__=="__main__":
    if os.name != 'nt':
        settings = termios.tcgetattr(sys.stdin)

    rospy.init_node('turtlebot3_camshift')
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    sub = rospy.Subscriber("camshift/track_box", RotatedRectStamped, callback, queue_size=1)

    auto = False  
    twist = Twist()
    
    while(1):
        key = getKey()
        if key == 'q' :
            auto = True  
        elif key == 'w' :
            auto = False
            twist.linear.x =  0.1
            twist.angular.z = 0.0
        elif key == 'x' :
            auto = False
            twist.linear.x = -0.1
            twist.angular.z = 0.0
        elif key == 'a' :
            auto = False
            twist.linear.x =  0.0
            twist.angular.z = 1.0
        elif key == 'd' :
            auto = False
            twist.linear.x =   0.0
            twist.angular.z = -1.0
        elif key == ' ' or key == 's' :
            auto = False
            twist.linear.x =  0.0
            twist.angular.z = 0.0
        else:
            if (key == '\x03'):
                break

        os.system('cls' if os.name == 'nt' else 'clear')
        print(msg)          
        
        if auto == True :
            print("Object x: %s" % (object_x_))
            twist.linear.x = 0.0
            if object_x_ > -1 and object_x_ < 200 :
                twist.angular.z = 0.5
            elif object_x_ > 440 :
                twist.angular.z = -0.5
            else:
                twist.angular.z = 0.0
        
        print("cmd_vel: linear.x: %.3f, angular.z: %.3f" % (twist.linear.x, twist.angular.z))
        pub.publish(twist)

    if os.name != 'nt':
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)