#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
import sys, select, os
if os.name == 'nt':
  import msvcrt
else:
  import tty, termios

from std_msgs.msg import String
from move_base_msgs.msg import MoveBaseActionGoal
from actionlib_msgs.msg import GoalID
from actionlib_msgs.msg import GoalStatusArray

voice_command_ = ""
goal_ = 0 #0:Not navigating, 1:Go to A, 2:Go to B, -1:Reach A, -2:Reach B...

msg = """
Control Your TurtleBot3!
---------------------------
Voice command:
Back: Go to point A
Move: Go to point B

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
    
def callbackVoice(data):
    global voice_command_
        
    voice_command_ = data.data
    
def callbackNav(data):
    global goal_
    if goal_ > 0 and len(data.status_list) == 1 and "Goal reached." in data.status_list[0].text :
        goal_ = -goal_    
 
if __name__=="__main__":
    if os.name != 'nt':
        settings = termios.tcgetattr(sys.stdin)

    rospy.init_node('tb3_navvoice')
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    pubNav = rospy.Publisher('/move_base/goal', MoveBaseActionGoal, queue_size=5)
    pubCancel = rospy.Publisher('/move_base/cancel', GoalID, queue_size=5)
    subVoice = rospy.Subscriber("recognizer/output", String, callbackVoice, queue_size=10)
    subNav = rospy.Subscriber("/move_base/status", GoalStatusArray, callbackNav, queue_size=1)
    
    navGoal = MoveBaseActionGoal()
    navGoal.goal.target_pose.header.frame_id = 'map'
    navCancel = GoalID()
    
    twist = Twist()
    
    while(1):
        key = getKey()
        if key == ' ' or key == 's' :
            pubCancel.publish(navCancel)
            goal_ = 0
            pub.publish(twist)
            voice_command_ = "" 
        else:
            if (key == '\x03'):
                break

        os.system('cls' if os.name == 'nt' else 'clear')
        print(msg)             
                
        if voice_command_ != "":
            print(voice_command_) 

        if "back" in voice_command_ :
            goal_ = 1
            navGoal.goal.target_pose.pose.position.x = 0.000
            navGoal.goal.target_pose.pose.position.y = 0.000
            navGoal.goal.target_pose.pose.orientation.z = 0.000
            navGoal.goal.target_pose.pose.orientation.w = 1.000
            pubNav.publish(navGoal)
        elif "move" in voice_command_ :
            navGoal.goal.target_pose.pose.position.x = 1.49000012875
            navGoal.goal.target_pose.pose.position.y = 1.12999987602
            navGoal.goal.target_pose.pose.orientation.z = 0.000
            navGoal.goal.target_pose.pose.orientation.w = 1.000
            pubNav.publish(navGoal)
        voice_command_ = "" 
 
        if goal_ == 1:
            print("Going to point A")
        elif goal_ == 2:
            print("Going to point B")
        elif goal_ == -1:
            print("Reach point A")
            pubCancel.publish(navCancel)
        elif goal_ == -2:
            print("Reach point B")
            pubCancel.publish(navCancel)
        else:
            print("Stop navigation")

    if os.name != 'nt':
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
