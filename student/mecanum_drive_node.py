#!/usr/bin/env python3
"""Part B: a ROS 2 node for the mecanum drive.

Start the simulator first, then this node in a second terminal:
    ros2 launch ohm_odometry mecanum.launch.py
    ros2 run ohm_odometry mecanum_drive_node.py

You only change the places marked TODO. Wheel order everywhere: front left, front right,
rear left, rear right.
"""
import math
import time

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped, PoseWithCovarianceStamped, Twist
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64MultiArray

# TODO 1: the topic names — the same kinds of topics as in part A.
TOPIC_ENCODERS = "TODO"     # wheel encoders              sensor_msgs/JointState
TOPIC_KEYBOARD = "TODO"     # what the keys ask for       geometry_msgs/Twist
TOPIC_TRUTH = "TODO"        # the true pose of the robot  geometry_msgs/PoseStamped
TOPIC_WHEELS = "TODO"       # wheel speeds for the robot  std_msgs/Float64MultiArray
TOPIC_ESTIMATE = "TODO"     # your pose (green outline)   geometry_msgs/PoseWithCovarianceStamped

LX = 0.14                   # half the distance front axle - rear axle [m]
LY = 0.13                   # half the distance left wheel - right wheel [m]
R = 0.05                    # wheel radius [m]
A = LX + LY


def inverse_kinematics(vx, vy, omega):
    """TODO 2: robot speed (vx, vy in m/s, omega in rad/s) -> four wheel speeds in rad/s.

    Script (1.39). Careful: the simulator counts every wheel positive when it rolls forward,
    the script counts the right wheels (omega_1, omega_3) the other way round (handout, task 3).
    """
    w_fl = (vx - vy - A * omega) / R           # given: row omega_0 of (1.39)
    w_fr = 0.0
    w_rl = 0.0
    w_rr = 0.0
    return w_fl, w_fr, w_rl, w_rr


def forward_kinematics(w_fl, w_fr, w_rl, w_rr):
    """TODO 3: four wheel speeds in rad/s -> robot speed (vx, vy, omega). Script (1.40), same signs."""
    vx = 0.0
    vy = 0.0
    omega = 0.0
    return vx, vy, omega


def odometry_step(x, y, phi, vx, vy, omega, dt):
    """TODO 4: the pose (x, y, phi) after driving dt seconds with (vx, vy, omega). Handout, equation (1)."""
    return x, y, phi


class MecanumDriveNode(Node):
    def __init__(self):
        super().__init__("mecanum_drive")
        self.create_subscription(JointState, TOPIC_ENCODERS, self.on_encoders, 10)
        self.create_subscription(Twist, TOPIC_KEYBOARD, self.on_keyboard, 10)
        self.create_subscription(PoseStamped, TOPIC_TRUTH, self.on_truth, 10)
        self.wheels_pub = self.create_publisher(Float64MultiArray, TOPIC_WHEELS, 10)
        self.estimate_pub = self.create_publisher(PoseWithCovarianceStamped, TOPIC_ESTIMATE, 10)
        self.create_timer(0.02, self.drive)        # 50 times per second
        self.pose = None                           # (x, y, phi) of the odometry
        self.last = None                           # (time, wheel angles) of the last encoder message
        self.key = (0.0, 0.0, 0.0)                 # (vx, vy, omega) from the keyboard
        self.key_time = 0.0

    def on_truth(self, msg):
        """The first true pose is where the odometry starts. After that it is not used."""
        if self.pose is None:
            phi = 2 * math.atan2(msg.pose.orientation.z, msg.pose.orientation.w)
            self.pose = (msg.pose.position.x, msg.pose.position.y, phi)

    def on_keyboard(self, msg):
        self.key = (msg.linear.x, msg.linear.y, msg.angular.z)
        self.key_time = time.time()

    def on_encoders(self, msg):
        """Wheel angles -> wheel speeds -> robot speed -> new pose."""
        t = msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9
        angles = list(msg.position)                # [fl, fr, rl, rr] in rad
        if self.pose is not None and self.last is not None and t > self.last[0]:
            dt = t - self.last[0]
            wheels = [(now - before) / dt for now, before in zip(angles, self.last[1])]
            vx, vy, omega = forward_kinematics(*wheels)
            self.pose = odometry_step(*self.pose, vx, vy, omega, dt)
            self.publish_estimate(msg.header.stamp)
        self.last = (t, angles)

    def command(self):
        """The (vx, vy, omega) to drive now: the keyboard. A key released for 0.3 s stops the robot."""
        return self.key if time.time() - self.key_time < 0.3 else (0.0, 0.0, 0.0)

    def drive(self):
        """50 times per second: command -> wheel speeds."""
        vx, vy, omega = self.command()
        wheels = inverse_kinematics(vx, vy, omega)
        self.wheels_pub.publish(Float64MultiArray(data=[float(w) for w in wheels]))

    def publish_estimate(self, stamp):
        x, y, phi = self.pose
        msg = PoseWithCovarianceStamped()
        msg.header.stamp = stamp
        msg.header.frame_id = "map"
        msg.pose.pose.position.x = float(x)
        msg.pose.pose.position.y = float(y)
        msg.pose.pose.orientation.z = math.sin(phi / 2)    # ROS stores the heading as a quaternion
        msg.pose.pose.orientation.w = math.cos(phi / 2)
        self.estimate_pub.publish(msg)


def main():
    if "TODO" in (TOPIC_ENCODERS, TOPIC_KEYBOARD, TOPIC_TRUTH, TOPIC_WHEELS, TOPIC_ESTIMATE):
        print("First TODO 1: fill in the topic names (ros2 topic list).")
        return
    rclpy.init()
    try:
        rclpy.spin(MecanumDriveNode())
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
