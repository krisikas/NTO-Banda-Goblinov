#!/usr/bin/env python

import rospy
from std_msgs.msg import String
import json
import random
import time

def cmd(msg):
    print(msg.data)

def simulator_publisher():
    rospy.Subscriber("/cmd/action", String, cmd)
    pub = rospy.Publisher('/tubes', String, queue_size=10)
    rospy.init_node('tubes_simulator_node', anonymous=True)
    rate = rospy.Rate(1) 


    rospy.loginfo("Starting tubes data simulator publisher...")

    while not rospy.is_shutdown():
        tube_data = [
            {"id": 1, "x": 1, "y": 1, "color": "red"},
            {"id": 2, "x": 1, "y": 1, "color": "blue"}
        ]
        
        json_string = json.dumps(tube_data)

        msg = String()
        msg.data = json_string

        pub.publish(msg)
        rospy.loginfo(f"Published mock tube data string.")
        
        rate.sleep()

if __name__ == '__main__':
    try:
        simulator_publisher()
    except rospy.ROSInterruptException:
        pass
