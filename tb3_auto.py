#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
import sys, select, os
if os.name == 'nt':
  import msvcrt
else:
  import tty, termios
  
from sensor_msgs.msg import LaserScan

lidar_FC_ = 0
lidar_FL_ = 0
lidar_FR_ = 0

msg = """
Control Your TurtleBot3!
---------------------------
Moving around:
        w
   a    s    d
        x
w : forward with lidar
x : backward
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
    global lidar_FC_, lidar_FL_, lidar_FR_
        
    if data.ranges[0] > data.range_min and data.ranges[0] < data.range_max:
        lidar_FC_ = data.ranges[0]

    if data.ranges[30] > data.range_min and data.ranges[30] < data.range_max:
        lidar_FL_ = data.ranges[30]

    if data.ranges[330] > data.range_min and data.ranges[330] < data.range_max:
        lidar_FR_ = data.ranges[330]    

if __name__=="__main__":
    if os.name != 'nt':
        settings = termios.tcgetattr(sys.stdin)

    rospy.init_node('turtlebot3_auto')
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    sub = rospy.Subscriber("scan", LaserScan, callback, queue_size=10)

    auto = False  
    twist = Twist()

    while(1):
        key = getKey()
        if key == 'w' :
            auto = True
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
            print("Lidar: %.3f, %.3f, %.3f" % (lidar_FL_, lidar_FC_, lidar_FR_))
            if lidar_FC_ > 0.6 and lidar_FL_ > 0.4 and lidar_FR_ > 0.4 :
                twist.linear.x =  0.1
                twist.angular.z = 0.0
            elif lidar_FL_ > lidar_FR_:
                twist.linear.x =  0.0
                twist.angular.z = 1.0
            else:
                twist.linear.x =   0.0
                twist.angular.z = -1.0
                
        print("cmd_vel: linear.x: %.3f, angular.z: %.3f" % (twist.linear.x, twist.angular.z))
        pub.publish(twist)

    if os.name != 'nt':
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)