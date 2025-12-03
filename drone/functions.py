#!/usr/bin/env python3
import math
import rospy
from mavros_msgs.srv import  CommandLongRequest


def navigate_wait(deps,
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
        check_cmd(deps)
        deps.navigate(
            x=x,
            y=y,
            z=z,
            yaw=yaw,
            speed=speed,
            frame_id=frame_id,
            auto_arm=auto_arm
        )
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


def check_cmd(deps, back = False, x=0, y=0, z=0):
    if deps.cmd == "kill":
        print("[drone] KILLING")
        rospy.wait_for_service('/mavros/cmd/command')
        try:
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
            
            response = deps.command_long_service(req)
            if response.success:
                print("[drone] KILLSWITCH SUCCESS")
            else:
                print("[drone] KILLSWITCH NOT SUCCESS")
        except rospy.ServiceException as e:
            print(f"[drone] KILLSWITCH ERROR: {e}")
        exit()
    elif deps.cmd == "stop":
        print("[drone] STOPPED")
        if not deps.stopped:
            deps.stopped = True
            navigate_wait_unstoppable(
                deps,
                x=0,
                y=0.5,
                z=0,
                frame_id="body"
            )
            deps.land()
            rospy.sleep(3)
        print("[drone] WAIT FOR START")
        while deps.cmd != "start":
            rospy.sleep(0.1)
    if deps.stopped:
        print("[drone] STARTING")
        deps.stopped = False
        navigate_wait_unstoppable(
            deps,
            x=0,
            y=0,
            z=1,
            frame_id="body",
            auto_arm=True
        )
        rospy.sleep(2)
        if back:
            navigate_wait_unstoppable(
                deps,
                x=x,
                y=y,
                z=z,
                frame_id="aruco_map",
                auto_arm=True
            )
            rospy.sleep(2)
        print("[drone] STARTED")