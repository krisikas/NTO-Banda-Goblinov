#!/usr/bin/env python3
import math
import rospy
import cv2
from sensor_msgs.msg import Image
from functions import navigate_wait, proj_point


def part(deps, tubes, start_point, end_point, isFirst):

    print("[clover] start scanning part")


    deps.navigate(
        x=end_point[0],
        y=end_point[1],
        z=1,
        speed=0.1,
        yaw=float('nan'),
        frame_id="aruco_map"
    )

    temp_tube = [0, 0, 0, 0] # format: dist angle mass cnt

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

            if area > temp_tube[2]:
                angle = (math.pi if M["m10"] / M["m00"] > 30 else 0) if isFirst else (math.pi*5/6 if M["m10"] / M["m00"] > 30 else -math.pi/6)
                temp_tube = [
                    telem.x if isFirst else proj_point((telem.x, telem.y), end_point, start_point), 
                    angle, 
                    area, 
                    1
                ]
            elif area == temp_tube[3]:
                if isFirst:
                    temp_tube[0] = (temp_tube[0] * temp_tube[3] + telem.x) / (temp_tube[3] + 1)
                else:
                    d = proj_point((telem.x, telem.y), end_point, start_point)
                    temp_tube[0] = (temp_tube[0] * temp_tube[3] + d) / (temp_tube[3] + 1)
                temp_tube[3] += 1

        elif temp_tube[3] != 0:
            if isFirst:
                cx, cy = temp_tube[0], 1
            else:
                cx, cy = start_point[0] + temp_tube[0]*math.cos(math.pi/6) , start_point[1] + temp_tube[0]*math.sin(math.pi/6)

            if len(tubes) == 0 or (((tubes[-1]["x"]-cx)**2)+((tubes[-1]["y"]-cy)**2))**0.5 >= 0.75:
                tubes.append({"x": cx, "y": cy, "angle": temp_tube[1]})
                temp_tube = [0, 0, 0, 0, 0]

        cv2.imshow('cropped', cropped)
        cv2.imshow('Filtered Result', result)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        print("[clover] scan {}: {} \n".format("first" if isFirst else "second", tubes))

    if temp_tube[2] != 0:
        tubes.append([temp_tube[0], temp_tube[1], temp_tube[2]])
        temp_tube = [0, 0, 0, 0, 0]


    print("[clover] END {} PART: {}".format("FIRST" if isFirst else "SECOND", tubes))
