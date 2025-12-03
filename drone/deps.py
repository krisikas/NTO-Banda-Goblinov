#!/usr/bin/env python3
import rospy
import numpy as np
from cv_bridge import CvBridge
from clover import srv
from std_srvs.srv import Trigger
from mavros_msgs.srv import CommandBool
from std_msgs.msg import String
from mavros_msgs.srv import CommandLong


class CloverDeps:
    def __init__(self, node_name="flight"):
        # Инициализация ROS-ноды
        rospy.init_node(node_name)

        # Границы по HSV для выделения объекта (труб) на изображении
        self.lower_bound = np.array([33, 0, 0])
        self.upper_bound = np.array([179, 255, 255])

        # Флаги и текущее состояние команды
        self.stopped = True
        self.cmd = "stop"

        # Сервисы Clover/ MAVROS
        self.get_telemetry = rospy.ServiceProxy("get_telemetry", srv.GetTelemetry)
        self.navigate = rospy.ServiceProxy("navigate", srv.Navigate)
        self.land = rospy.ServiceProxy("land", Trigger)
        self.arming = rospy.ServiceProxy("mavros/cmd/arming", CommandBool)
        self.command_long_service = rospy.ServiceProxy('/mavros/cmd/command', CommandLong)

        # Бридж для конвертации ROS Image <=> OpenCV
        self.bridge = CvBridge()

        # Паблишеры для труб и статуса
        self.tubes_pub = rospy.Publisher("/tubes", String, queue_size=1)
        self.status_pub = rospy.Publisher("/status", String, queue_size=1)

        # Подписка на топик команд управления
        rospy.Subscriber('/cmd', String, self.cmd_callback)

    def cmd_callback(self, data):
        # Обновляем текущую команду (start/stop/kill)
        self.cmd = str(data.data)
