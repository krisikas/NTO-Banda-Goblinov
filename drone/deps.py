#!/usr/bin/env python3
import rospy
import numpy as np
from cv_bridge import CvBridge
from clover import srv
from std_srvs.srv import Trigger
from mavros_msgs.srv import CommandBool
from std_msgs.msg import String
from functions import navigate_wait


class CloverDeps:
    def __init__(self, node_name="flight"):
        rospy.init_node(node_name)

        self.get_telemetry = rospy.ServiceProxy("get_telemetry", srv.GetTelemetry)
        self.navigate = rospy.ServiceProxy("navigate", srv.Navigate)
        self.land = rospy.ServiceProxy("land", Trigger)
        self.arming = rospy.ServiceProxy("mavros/cmd/arming", CommandBool)

        self.bridge = CvBridge()

        self.tubes_pub = rospy.Publisher("/tubes", String, queue_size=1)
        self.tubes_pub.publish("[]")

        rospy.Subscriber('/cmd', String, self.cmd_callback)

        self.lower_bound = np.array([33, 0, 0])
        self.upper_bound = np.array([179, 255, 255])

        self.stopped = True

    def cmd_callback(self, data):
        self.cmd = data

    def check_cmd(self):
        if self.cmd == "kill":
            print("[clover] KILLING")
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
                    print("[clover] KILL SUCCESS")
                else:
                    print("[clover] KILL NOT SUCCESS")
            except rospy.ServiceException as e:
                print(f"[clover] KILL ERROR: {e}")
            exit()
        elif self.cmd == "stop":
            print("[clover] STOPPED")
            self.stopped = True
            navigate_wait(
                self,
                x=1,
                y=0,
                z=0,
                frame_id="body"
            )
            land()

            print("[clover] WAIT FOR START")
            while self.cmd != "start":
                pass
        if stopped:
            navigate_wait(
                self,
                x=0,
                y=0,
                z=1,
                frame_id="body",
                auto_arm=True
            )


