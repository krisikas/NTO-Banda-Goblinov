#!/usr/bin/env python3
import rospy
import numpy as np
from cv_bridge import CvBridge
from clover import srv
from std_srvs.srv import Trigger
from mavros_msgs.srv import CommandBool


class CloverDeps:
    def __init__(self, node_name='flight'):
        rospy.init_node(node_name)

        self.get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
        self.navigate = rospy.ServiceProxy('navigate', srv.Navigate)
        self.land = rospy.ServiceProxy('land', Trigger)
        self.arming = rospy.ServiceProxy('mavros/cmd/arming', CommandBool)

        self.bridge = CvBridge()

        # HSV-границы для поиска труб
        self.lower_bound = np.array([33, 0, 0])
        self.upper_bound = np.array([179, 255, 255])
