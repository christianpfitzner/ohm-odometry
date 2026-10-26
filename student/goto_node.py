#!/usr/bin/env python3
"""Extra task E2: drive to a point.

This node is your node from tasks 1 to 4 with one change: the command does not come from the
keyboard but from command() below. Your kinematics and your odometry are used as they are, so finish
those first.

Start the simulator for your own node, then this node instead of your drive node:
    ros2 launch ohm_odometry diff.launch.py
    ros2 run ohm_odometry goto_node.py

You only change the places marked TODO.
"""
import math

import rclpy

ROBOT = "diff"              # "diff" or "mecanum": which of your nodes drives to the goal

if ROBOT == "diff":
    import diff_drive_node as base
    Node = base.DiffDriveNode
else:
    import mecanum_drive_node as base
    Node = base.MecanumDriveNode

GOAL_AHEAD = 2.0            # the goal, seen from the start pose: 2 m ahead ... [m]
GOAL_LEFT = 1.0             # ... and 1 m to the left [m]
K_RHO = 0.5                 # [1/s]
K_ALPHA = 1.5               # [1/s]
V_MAX = 0.3                 # [m/s]
REACHED = 0.05              # [m]


def wrap(angle):
    """The angle in (-pi, pi]."""
    return math.atan2(math.sin(angle), math.cos(angle))


class GotoNode(Node):
    def __init__(self):
        super().__init__()
        self.goal = None        # (x_g, y_g) in the hall, set from the first pose

    def command(self):
        """The command for this moment, from your odometry self.pose = (x, y, phi)."""
        stop = (0.0, 0.0) if ROBOT == "diff" else (0.0, 0.0, 0.0)
        if self.pose is None:
            return stop
        x, y, phi = self.pose
        if self.goal is None:   # the goal relative to the start pose, turned into the hall
            self.goal = (x + GOAL_AHEAD * math.cos(phi) - GOAL_LEFT * math.sin(phi),
                         y + GOAL_AHEAD * math.sin(phi) + GOAL_LEFT * math.cos(phi))
            self.get_logger().info(f"goal at ({self.goal[0]:.2f}, {self.goal[1]:.2f})")
        x_g, y_g = self.goal

        dx = 0.0                # TODO E2a: the error in the hall and its length rho, handout eq. (3)
        dy = 0.0
        rho = 0.0
        if rho < REACHED:
            return stop

        if ROBOT == "diff":
            alpha = 0.0         # TODO E2b: angle to the goal, handout eq. (4)
            v = 0.0
            omega = 0.0
            return (min(v, V_MAX), omega)

        e_x = 0.0               # TODO E2c: the error in the frame of the robot, handout eq. (5)
        e_y = 0.0
        vx, vy = K_RHO * e_x, K_RHO * e_y
        speed = math.hypot(vx, vy)
        if speed > V_MAX:       # keep the direction, limit the speed
            vx, vy = vx * V_MAX / speed, vy * V_MAX / speed
        return (vx, vy, 0.0)


def main():
    if "TODO" in (base.TOPIC_ENCODERS, base.TOPIC_KEYBOARD, base.TOPIC_TRUTH, base.TOPIC_WHEELS,
                  base.TOPIC_ESTIMATE):
        print(f"First TODO 1 in {base.__name__}.py: fill in the topic names.")
        return
    rclpy.init()
    try:
        rclpy.spin(GotoNode())
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
