"""Task 0, the diff robot: the simulator with its own kinematics — the keys drive, no node of yours.

    ros2 launch ohm_odometry diff_demo.launch.py
"""
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))   # checkout, even via a symlink
if HERE not in sys.path:
    sys.path.append(HERE)
from ohm_odometry.launching import describe                     # noqa: E402


def generate_launch_description():
    return describe("diff", "diff_drive_node.py", demo=True)
