#!/usr/bin/env python3
import math
import rospy

from deps import CloverDeps
from functions import navigate_wait
from first_part import first_part
from second_part import second_part
deps = CloverDeps(node_name='flight')

first_start_point = (1, 1)
fist_end_point = (5.2, 1)
second_start_point = (5, 1)
second_end_poinny = (5+math.cos(math.pi/6)*4.2, 1+math.sin(math.pi/6)*4.2)


def main():

    print("[clover] fly to start")

    navigate_wait(
        deps,
        x=0,
        y=0,
        z=1,
        frame_id="body",
        auto_arm=True
    )

    navigate_wait(
        deps,
        x=1,
        y=4,
        z=1,
        frame_id="aruco_map"
    )
    rospy.sleep(3)

    first_part(deps, tubes, first_start_point, fist_end_point)
    rospy.sleep(3)

    navigate_wait(
        deps,
        x=5,
        y=4,
        z=1,
        frame_id="aruco_map"
    )
    rospy.sleep(3)

    second_part(deps, tubes, first_start_point, fist_end_point)
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


if __name__ == "__main__":
    main()
