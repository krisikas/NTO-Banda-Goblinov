#!/usr/bin/env python3
import math
import rospy

from deps import CloverDeps
from functions import navigate_wait
from part import part

deps = CloverDeps(node_name='flight')

first_start_point = (1, 1)
fist_end_point = (5.2, 1)
second_start_point = (5, 1)
second_end_point = (5+math.cos(math.pi/6)*4.2, 1+math.sin(math.pi/6)*4.2)

tubes = [] # format: array [{x:float, y:float, angle:float(rad)}, {}]

def main():

    rospy.sleep(5)
    
    deps.tubes_pub.publish("[]")
    deps.status_pub.publish("stop")

    deps.check_cmd()

    print("[drone] fly to start")

    navigate_wait(
        deps,
        x=first_start_point[0],
        y=first_start_point[1],
        z=1,
        yaw= 0,
        frame_id="aruco_map"
    )
    deps.check_cmd()

    rospy.sleep(3)

    part(deps, tubes, first_start_point, fist_end_point, True)
    deps.check_cmd()

    rospy.sleep(3)

    navigate_wait(
        deps,
        x=second_start_point[0],
        y=second_start_point[1],
        yaw=math.pi / 6,
        z=1,
        frame_id="aruco_map"
    )
    deps.check_cmd()

    rospy.sleep(3)

    part(deps, tubes, second_start_point, second_end_point, False)
    deps.check_cmd()

    rospy.sleep(3)

    navigate_wait(
        deps,
        x=0,
        y=0,
        z=1,
        frame_id="aruco_map"
    )
    rospy.sleep(1)

    deps.land()
    rospy.sleep(3)
    deps.status_pub.publish("end")


if __name__ == "__main__":
    main()
