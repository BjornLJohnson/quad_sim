#!/usr/bin/env python

import roslib; roslib.load_manifest('teleop_twist_keyboard')
import rospy

from geometry_msgs.msg import Twist
from quadrotor_msgs.msg import SO3Command

import sys, select, termios, tty, rospy
import curses

robot_name = "quad01"

msg = """
Reading from the keyboard and Publishing to so3_cmd!
---------------------------
Moving options:
---------------------------
   w -- up (+z)
   s -- down (-z)
   a -- counter clockwise yaw
   d -- clockwise yaw
   up arrow -- forward (+x)
   down arrow -- backward (-x)
   <- -- forward (+y)
   -> -- backward (-y)
   CTRL-C to quit
"""
print(msg)

hover_force = rospy.get_param("~hover_force", 4.5)
f_mult = rospy.get_param("~f_mult" , 1.5) 
w_mult = rospy.get_param("~w_mult", 2)


def getKey():
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.2)
    if rlist:
        key = sys.stdin.read(1)
        ### if using arrow keys, need to retrieve 3 keys in buffer
        if ord(key) == 27:
            key = sys.stdin.read(1)
        if ord(key) == 91:
               key = sys.stdin.read(1)
    else:
        key = ''
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


if __name__=="__main__":
    settings = termios.tcgetattr(sys.stdin)
    rospy.init_node('teleop_twist_keyboard')
    pub = rospy.Publisher('so3_cmd', SO3Command, queue_size = 1)
    rate = rospy.Rate(20) # 10hz

    while not rospy.is_shutdown():
        fx = 0
        fy = 0
        fz = hover_force
        wx = 0
        wy = 0
        wz = 0
        key = getKey()
        
        if key == 'w':
            fz = fz+f_mult
        elif key == 's':
            fz = fz-f_mult
        if key == 'a':
            wz = w_mult
        elif key == 'd':
            wz = -w_mult
        if key=='A':
            wx = w_mult
        elif key=='B':
            wx = -w_mult
        if key=='C':
            wy = -w_mult
        elif key=='D':
            wy = w_mult
            if (key == '\x03'):
                break
        
        cmd = SO3Command()
        cmd.force.x = fx
        cmd.force.y = fy
        cmd.force.z = fz
        cmd.angular_velocity.x = wx
        cmd.angular_velocity.y = wy
        cmd.angular_velocity.z = wz
        cmd.kR = [1,1,1]
        cmd.kOm = [1,1,1]
        cmd.aux.enable_motors = True
        
        pub.publish(cmd)
        rate.sleep()