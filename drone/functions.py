#!/usr/bin/env python3
import math
import rospy


def navigate_wait(deps,
                  x=0, y=0, z=0,
                  yaw=float('nan'),
                  speed=0.3,
                  frame_id='',
                  auto_arm=False,
                  tolerance=0.1):
    

    while not rospy.is_shutdown():
        deps.navigate(
            x=x,
            y=y,
            z=z,
            yaw=yaw,
            speed=speed,
            frame_id=frame_id,
            auto_arm=auto_arm
        )
        telem = deps.get_telemetry(frame_id='navigate_target')
        print(math.sqrt(telem.x ** 2 + telem.y ** 2 + telem.z ** 2))
        if math.sqrt(telem.x ** 2 + telem.y ** 2 + telem.z ** 2) < tolerance:
            break
        deps.check_cmd()
        rospy.sleep(0.1)

def navigate_wait_unstoppable(deps,
                  x=0, y=0, z=0,
                  yaw=float('nan'),
                  speed=0.3,
                  frame_id='',
                  auto_arm=False,
                  tolerance=0.1):
    deps.navigate(
        x=x,
        y=y,
        z=z,
        yaw=yaw,
        speed=speed,
        frame_id=frame_id,
        auto_arm=auto_arm
    )
    

    while not rospy.is_shutdown():
        telem = deps.get_telemetry(frame_id='navigate_target')
        if math.sqrt(telem.x ** 2 + telem.y ** 2 + telem.z ** 2) < tolerance:
            break
        rospy.sleep(0.1)

def proj_point(pos, A, B):
    AB = (B[0] - A[0], B[1] - A[1])
    BP = (pos[0] - B[0], pos[1] - B[1])

    normAB = math.hypot(*AB)
    return -(AB[0] * BP[0] + AB[1] * BP[1]) / normAB
