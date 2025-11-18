import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import numpy as np
import math
from clover import srv
from std_srvs.srv import Trigger
from std_msgs.msg import String
from threading import Thread
from mavros_msgs.srv import CommandBool
from time import sleep

lower_bound = np.array([33, 0, 0])
upper_bound = np.array([179, 255, 255])

rospy.init_node('flight')

get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
land = rospy.ServiceProxy('land', Trigger)
arming = rospy.ServiceProxy('mavros/cmd/arming', CommandBool)

bridge = CvBridge()

# Функция навигации с ожиданием достижения цели
def navigate_wait(x=0, y=0, z=0, yaw=float('nan'), speed=0.3, frame_id='', auto_arm=False, tolerance=0.1):
    navigate(x=x, y=y, z=z, yaw=yaw, speed=speed, frame_id=frame_id, auto_arm=auto_arm)

    while not rospy.is_shutdown():
        telem = get_telemetry(frame_id='navigate_target')
        if math.sqrt(telem.x ** 2 + telem.y ** 2 + telem.z ** 2) < tolerance:
            break
        rospy.sleep(0.2)

def dist_point(pos, A, B):
    AB = (B[0] - A[0], B[1] - A[1])
    BP = (pos[0] - B[0], pos[1] - B[1])

    normAB = math.hypot(*AB)
    return -(AB[0]*BP[0] + AB[1]*BP[1])/(normAB)

def first_part():
    print(f"[clover] start scanning first part")
    start_point = (1, 4)
    end_point = (5.2, 4)
    navigate(x=end_point[0], y=end_point[1], z=1, speed=0.12, frame_id="aruco_map")

    coords_tubes = []
    temp_coords = [0, 0, 0, 0] # [mass, x, cnt, left/right: -1/1]

    while not rospy.is_shutdown():
        image = bridge.imgmsg_to_cv2(rospy.wait_for_message('main_camera/image_raw', Image), 'bgr8')
        telem_target = get_telemetry(frame_id='navigate_target')
        telem = get_telemetry(frame_id='aruco_map')
        if math.sqrt(telem_target.x ** 2 + telem_target.y ** 2 + telem_target.z ** 2) < 0.1:
            break
        if image is None:
            continue
        
        cropped = image[117:133, 130:190]
        hsv = cv2.cvtColor(cropped, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_bound, upper_bound)
        result = cv2.bitwise_and(cropped, cropped, mask=mask)
        
        contrs, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contrs:
            contr = max(contrs, key=cv2.contourArea)
            M = cv2.moments(contr)
            area = M['m00']
            print(f"{area:.2f}", f"{telem.x:.2f}")
            if area > temp_coords[0]:
                temp_coords = [area, telem.x, 1, 1 if M["m10"] / M["m00"] > 30 else -1]
            elif area == temp_coords[0]:
                temp_coords[1] = (temp_coords[1]*temp_coords[2] + telem.x)/(temp_coords[2]+1)
                temp_coords[2] = temp_coords[2]+1
        elif temp_coords[2] != 0:
            coords_tubes.append([temp_coords[1], 4, temp_coords[3]])
            temp_coords = [0, 0, 0, 0]



        cv2.imshow('cropped', cropped)
        cv2.imshow('HSV Mask', mask)
        cv2.imshow('Filtered Result', result)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        print(f"[clover] scan first part: {coords_tubes} \n")

    if temp_coords[2] != 0:
        coords_tubes.append([temp_coords[1], 4, temp_coords[3]])
        temp_coords = [0, 0, 0, 0]
    navigate_wait(5, 4, 1, yaw = -math.pi/6,  speed=0.12, frame_id="aruco_map")
    print(f"[clover] end first part: {coords_tubes}")

def second_part():
    print(f"[clover] start scanning second part")
    start_point = (5, 4)
    end_point = (5+math.cos(math.pi/6)*4.2, 4-math.sin(math.pi/6)*4.2)
    navigate(x=end_point[0], y=end_point[1], z=1, yaw=float('nan'), speed=0.12, frame_id="aruco_map")

    coords_tubes = []
    temp_coords = [0, 0, 0, 0] # [mass, x, cnt, left/right: -1/1]

    while not rospy.is_shutdown():
        image = bridge.imgmsg_to_cv2(rospy.wait_for_message('main_camera/image_raw', Image), 'bgr8')
        telem_target = get_telemetry(frame_id='navigate_target')
        telem = get_telemetry(frame_id='aruco_map')
        if math.sqrt(telem_target.x ** 2 + telem_target.y ** 2 + telem_target.z ** 2) < 0.1:
            break
        if image is None:
            continue
        
        cropped = image[117:133, 130:190]
        hsv = cv2.cvtColor(cropped, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_bound, upper_bound)
        result = cv2.bitwise_and(cropped, cropped, mask=mask)
        
        contrs, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contrs:
            contr = max(contrs, key=cv2.contourArea)
            M = cv2.moments(contr)
            area = M['m00']
            print(f"{area:.2f}", f"{telem.x:.2f}")
            if area > temp_coords[0]:
                temp_coords = [area, dist_point((telem.x, telem.y), end_point, start_point), 1, 1 if M["m10"] / M["m00"] > 30 else -1]
            elif area == temp_coords[0]:
                temp_coords[1] = (temp_coords[1]*temp_coords[2] + dist_point((telem.x, telem.y), end_point, start_point))/(temp_coords[2]+1)
                temp_coords[2] = temp_coords[2]+1
        elif temp_coords[2] != 0:
            coords_tubes.append([temp_coords[1], 4, temp_coords[3]])
            temp_coords = [0, 0, 0, 0]



        cv2.imshow('cropped', cropped)
        cv2.imshow('HSV Mask', mask)
        cv2.imshow('Filtered Result', result)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        print(f"[clover] scan second part: {coords_tubes} \n")

    print(f"[clover] end second part: {coords_tubes}")

def main():
    print(f"[clover] fly to start")
    navigate_wait(0, 0, 1, frame_id="body", auto_arm=True)
    navigate_wait(1, 4, 1, frame_id="aruco_map")
    rospy.sleep(3)

    first_part()
    rospy.sleep(3)
    navigate_wait(5+math.cos(math.pi/6)*0.35, 4-math.sin(math.pi/6)*0.35, 1, frame_id="aruco_map")
    rospy.sleep(3)

    second_part()
    rospy.sleep(3)

    navigate_wait(0, 0, 1, frame_id="aruco_map")
    land()

    

if __name__ == "__main__":
    main()

# navigate_wait(6.73, 3, 2, -0.52, speed=0.5, auto_arm=True)
# rospy.sleep(2)
# img = bridge.imgmsg_to_cv2(rospy.wait_for_message('main_camera/image_raw', Image), 'bgr8') # Получение изображения

# cv2.imwrite("image2.png", img)