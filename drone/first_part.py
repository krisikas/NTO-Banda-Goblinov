#!/usr/bin/env python3
import math
import rospy
import cv2
from sensor_msgs.msg import Image
from functions import navigate_wait


def first_part(deps, tubes, start_point, end_point):

    print("[clover] start scanning first part")


    deps.navigate(
        x=end_point[0],
        y=end_point[1],
        z=1,
        speed=0.12,
        frame_id="aruco_map"
    )

    temp_tube = [0, 0, 0, 0]

    while not rospy.is_shutdown():
        image_msg = rospy.wait_for_message('main_camera/image_raw', Image)
        image = deps.bridge.imgmsg_to_cv2(image_msg, 'bgr8')

        telem_target = deps.get_telemetry(frame_id='navigate_target')
        telem = deps.get_telemetry(frame_id='aruco_map')

        if math.sqrt(telem_target.x ** 2 + telem_target.y ** 2 + telem_target.z ** 2) < 0.1:
            break
        if image is None:
            continue

        cropped = image[117:133, 130:190]
        hsv = cv2.cvtColor(cropped, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, deps.lower_bound, deps.upper_bound)
        result = cv2.bitwise_and(cropped, cropped, mask=mask)

        contrs, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        if contrs:
            contr = max(contrs, key=cv2.contourArea)
            M = cv2.moments(contr)
            area = M['m00']

            print(f"{area:.2f}", f"{telem.x:.2f}")

            if area > temp_coords[0]:
                side = 1 if M["m10"] / M["m00"] > 30 else -1
                temp_coords = [area, telem.x, 1, side]
            elif area == temp_coords[0]:
                temp_coords[1] = (temp_coords[1] * temp_coords[2] + telem.x) / (temp_coords[2] + 1)
                temp_coords[2] += 1

        elif temp_coords[2] != 0:
            coords_tubes.append([temp_coords[1], 4, temp_coords[3]])
            temp_coords = [0, 0, 0, 0]

        cv2.imshow('cropped', cropped)
        cv2.imshow('HSV Mask', mask)
        cv2.imshow('Filtered Result', result)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        print(f"[clover] scan first part: {coords_tubes} \n")

    # Если в конце цикла остался "висящий" объект
    if temp_coords[2] != 0:
        coords_tubes.append([temp_coords[1], 4, temp_coords[3]])
        temp_coords = [0, 0, 0, 0]

    # Поворачиваемся для второй части
    navigate_wait(
        deps,
        x=5,
        y=4,
        z=1,
        yaw=-math.pi / 6,
        speed=0.12,
        frame_id="aruco_map"
    )

    print(f"[clover] end first part: {coords_tubes}")
