#!/usr/bin/env python

import rospy
from quadrotor_msgs.msg import PositionCommand
from std_msgs.msg import Bool

robot_name = "quad01"

msg = """
Generating Parametric Trajectory and Publishing to pos_cmd!
"""
print(msg)

def getCommand():
    cmd = PositionCommand()

    cmd.position.x = 0
    cmd.position.y = 0
    cmd.position.z = 3

    cmd.velocity.x = 0
    cmd.velocity.y = 0
    cmd.velocity.z = 0
    
    cmd.acceleration.x = 0
    cmd.acceleration.y = 0
    cmd.acceleration.z = 0

    cmd.jerk.x = 0
    cmd.jerk.y = 0
    cmd.jerk.z = 0

    cmd.yaw = 0
    cmd.yaw_dot = 0

    cmd.kx = [1,1,1]
    cmd.kv = [.5,.5,.5]

    return cmd

if __name__=="__main__":
    rospy.init_node('hover_cmd')
    pub = rospy.Publisher('position_cmd', PositionCommand, queue_size = 10)
    rate = rospy.Rate(20) # 10hz

    motorPub = rospy.Publisher('motors', Bool, queue_size = 10)
    enable = Bool()
    enable.data = True
    rospy.sleep(1)
    motorPub.publish(enable)
        
    while not rospy.is_shutdown():
        pub.publish(getCommand())
        rate.sleep()