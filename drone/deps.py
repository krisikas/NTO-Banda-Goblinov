#!/usr/bin/env python3
import rospy
import numpy as np
from cv_bridge import CvBridge
from clover import srv
from std_srvs.srv import Trigger
from mavros_msgs.srv import CommandBool
from mavros_msgs.srv import CommandLong, CommandLongRequest
from std_msgs.msg import String
from functions import navigate_wait, navigate_wait_unstoppable
import threading
import time

class CloverDeps:
    def __init__(self, node_name="flight"):
        rospy.init_node(node_name)

        self.lower_bound = np.array([33, 0, 0])
        self.upper_bound = np.array([179, 255, 255])

        self.stopped = True
        self.cmd = "stop"

        self.get_telemetry = rospy.ServiceProxy("get_telemetry", srv.GetTelemetry)
        self.navigate = rospy.ServiceProxy("navigate", srv.Navigate)
        self.land = rospy.ServiceProxy("land", Trigger)
        self.arming = rospy.ServiceProxy("mavros/cmd/arming", CommandBool)

        self.bridge = CvBridge()

        self.tubes_pub = rospy.Publisher("/tubes", String, queue_size=1)
        self.status_pub = rospy.Publisher("/status", String, queue_size=1)

        rospy.Subscriber('/cmd', String, self.cmd_callback)


    def cmd_callback(self, data):
        self.cmd = str(data.data)

    def check_cmd(self, back = False, x=0, y=0, z=0):
        if self.cmd == "kill":
            print("[drone] KILLING")
            rospy.wait_for_service('/mavros/cmd/command')
            try:
                command_long_service = rospy.ServiceProxy('/mavros/cmd/command', CommandLong)
                
                req = CommandLongRequest()
                req.broadcast = False
                req.command = 400
                req.confirmation = 0
                req.param1 = 0.0
                req.param2 = 21196.0
                req.param3 = 0.0
                req.param4 = 0.0
                req.param5 = 0.0
                req.param6 = 0.0
                req.param7 = 0.0
            
                response = command_long_service(req)
                if response.success:
                    print("[drone] KILLSWITCH SUCCESS")
                else:
                    print("[drone] KILLSWITCH NOT SUCCESS")
            except rospy.ServiceException as e:
                print(f"[drone] KILLSWITCH ERROR: {e}")
            exit()
        elif self.cmd == "stop":
            print("[drone] STOPPED")
            if not self.stopped:
                self.stopped = True
                navigate_wait_unstoppable(
                    self,
                    x=0,
                    y=1,
                    z=0,
                    frame_id="body"
                )
                self.land()

            print("[drone] WAIT FOR START")
            while self.cmd != "start":
                rospy.sleep(0.1)
        if self.stopped:
            print("[drone] STARTING")
            self.stopped = False
            navigate_wait_unstoppable(
                self,
                x=0,
                y=0,
                z=1,
                frame_id="body",
                auto_arm=True
            )
            rospy.sleep(2)
            if back:
                navigate_wait_unstoppable(
                    self,
                    x=x,
                    y=y,
                    z=z,
                    frame_id="aruco_map",
                )
                rospy.sleep(2)
            print("[drone] STARTED")


