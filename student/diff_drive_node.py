#!/usr/bin/env python3
"""Part A: a ROS 2 node for the differential drive.

Start the simulator first, then this node in a second terminal:
    ros2 launch ohm_odometry diff.launch.py
    ros2 run ohm_odometry diff_drive_node.py

You only change the places marked TODO.
"""
import math
import time

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped, PoseWithCovarianceStamped, Twist
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64MultiArray

# TODO 1: the topic names. Find them with `ros2 topic list` while the simulator runs.
TOPIC_ENCODERS = "TODO"     # wheel encoders              sensor_msgs/JointState
TOPIC_KEYBOARD = "TODO"     # what the keys ask for       geometry_msgs/Twist
TOPIC_TRUTH = "TODO"        # the true pose of the robot  geometry_msgs/PoseStamped
TOPIC_WHEELS = "TODO"       # wheel speeds for the robot  std_msgs/Float64MultiArray
TOPIC_ESTIMATE = "TODO"     # your pose (green outline)   geometry_msgs/PoseWithCovarianceStamped

B = 0.30                    # track: distance between the two wheels [m]
R = 0.05                    # wheel radius [m]


def inverse_kinematics(v, omega):
    """TODO 2: robot speed (v in m/s, omega in rad/s) -> wheel speeds in rad/s. Script (1.30)."""
    w_left = 0.0
    w_right = 0.0
    return w_left, w_right


def forward_kinematics(w_left, w_right):
    """TODO 3: wheel speeds in rad/s -> robot speed (v in m/s, omega in rad/s). Script (1.30)."""
    v = 0.0
    omega = 0.0
    return v, omega


def odometry_step(x, y, phi, v, omega, dt):
    """TODO 4: the pose (x, y, phi) after driving dt seconds with (v, omega). Script (1.27)-(1.29)."""
    return x, y, phi


class DiffDriveNode(Node):
    def __init__(self):
        super().__init__("diff_drive")
        self.create_subscription(JointState, TOPIC_ENCODERS, self.on_encoders, 10)
        self.create_subscription(Twist, TOPIC_KEYBOARD, self.on_keyboard, 10)
        self.create_subscription(PoseStamped, TOPIC_TRUTH, self.on_truth, 10)
        self.wheels_pub = self.create_publisher(Float64MultiArray, TOPIC_WHEELS, 10)
        self.estimate_pub = self.create_publisher(PoseWithCovarianceStamped, TOPIC_ESTIMATE, 10)
        self.create_timer(0.02, self.drive)        # 50 times per second
        self.pose = None                           # (x, y, phi) of the odometry
        self.last = None                           # (time, wheel angles) of the last encoder message
        self.key = (0.0, 0.0)                      # (v, omega) from the keyboard
        self.key_time = 0.0

    def on_truth(self, msg):
        """The first true pose is where the odometry starts. After that it is not used."""
        if self.pose is None:
            phi = 2 * math.atan2(msg.pose.orientation.z, msg.pose.orientation.w)
            self.pose = (msg.pose.position.x, msg.pose.position.y, phi)

    def on_keyboard(self, msg):
        self.key = (msg.linear.x, msg.angular.z)
        self.key_time = time.time()

    def on_encoders(self, msg):
        """Wheel angles -> wheel speeds -> robot speed -> new pose."""
        t = msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9
        angles = list(msg.position)                # [left, right] in rad
        if self.pose is not None and self.last is not None and t > self.last[0]:
            dt = t - self.last[0]
            w_left = (angles[0] - self.last[1][0]) / dt
            w_right = (angles[1] - self.last[1][1]) / dt
            v, omega = forward_kinematics(w_left, w_right)
            self.pose = odometry_step(*self.pose, v, omega, dt)
            self.publish_estimate(msg.header.stamp)
        self.last = (t, angles)

    def command(self):
        """The (v, omega) to drive now: the keyboard. A key released for 0.3 s stops the robot."""
        return self.key if time.time() - self.key_time < 0.3 else (0.0, 0.0)

    def drive(self):
        """50 times per second: command -> wheel speeds."""
        v, omega = self.command()
        w_left, w_right = inverse_kinematics(v, omega)
        self.wheels_pub.publish(Float64MultiArray(data=[float(w_left), float(w_right), 0.0, 0.0]))

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
        rclpy.spin(DiffDriveNode())
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
