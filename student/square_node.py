#!/usr/bin/env python3
"""Extra task E1: drive a square by odometry.

This node is your node from tasks 1 to 4 with one change: the command does not come from the
keyboard but from command() below. Your kinematics and your odometry are used as they are, so finish
those first.

Start the simulator for your own node, then this node instead of your drive node:
    ros2 launch ohm_odometry diff.launch.py
    ros2 run ohm_odometry square_node.py

You only change the places marked TODO.
"""
import math

import rclpy

ROBOT = "diff"              # "diff" or "mecanum": which of your nodes drives the square

if ROBOT == "diff":
    import diff_drive_node as base
    Node = base.DiffDriveNode
else:
    import mecanum_drive_node as base
    Node = base.MecanumDriveNode

SIDE = 1.0                  # side length a [m]
SPEED = 0.2                 # [m/s]
TURN = 0.5                  # [rad/s]
MECANUM_SIDES = [(SPEED, 0.0), (0.0, SPEED), (-SPEED, 0.0), (0.0, -SPEED)]   # (vx, vy) per side


def wrap(angle):
    """The angle in (-pi, pi]."""
    return math.atan2(math.sin(angle), math.cos(angle))


class SquareNode(Node):
    def __init__(self):
        super().__init__()
        self.step = 0           # differential drive: side, corner, side, ... (8 steps); mecanum: 4 sides
        self.start = None       # (x, y, phi) at the start of the current step

    def next_step(self):
        self.step += 1
        self.start = None

    def command(self):
        """The command for this moment, from your odometry self.pose = (x, y, phi)."""
        stop = (0.0, 0.0) if ROBOT == "diff" else (0.0, 0.0, 0.0)
        steps = 8 if ROBOT == "diff" else 4
        if self.pose is None or self.step >= steps:
            return stop
        if self.start is None:
            self.start = self.pose
        x, y, phi = self.pose
        x_s, y_s, phi_s = self.start

        if ROBOT == "mecanum" or self.step % 2 == 0:          # a side
            d = 0.0             # TODO E1a: distance driven since self.start, handout eq. (2)
            if d >= SIDE:
                self.next_step()
                return stop
            if ROBOT == "diff":
                return (SPEED, 0.0)
            vx, vy = MECANUM_SIDES[self.step]
            return (vx, vy, 0.0)

        turned = 0.0            # TODO E1b: angle turned since self.start, use wrap()
        if abs(turned) >= math.pi / 2:
            self.next_step()
            return stop
        return (0.0, TURN)


def main():
    if "TODO" in (base.TOPIC_ENCODERS, base.TOPIC_KEYBOARD, base.TOPIC_TRUTH, base.TOPIC_WHEELS,
                  base.TOPIC_ESTIMATE):
        print(f"First TODO 1 in {base.__name__}.py: fill in the topic names.")
        return
    rclpy.init()
    try:
        rclpy.spin(SquareNode())
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
