"""Lab "Kinematics and odometry", part B: the simulator waits for the wheel speeds of your node.

    ros2 launch ohm_odometry mecanum.launch.py                  # simulator, window, RViz: the robot stands
    ros2 run ohm_odometry mecanum_drive_node.py                 # your node, in a second terminal
    ros2 launch launch/mecanum.launch.py                        # from the checkout, before a build

`--show-args` lists the arguments; ohm_odometry/launching.py does the work for both drive trains.
"""
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))   # checkout, even via a symlink
if HERE not in sys.path:
    sys.path.append(HERE)
from ohm_odometry.launching import describe                     # noqa: E402


def generate_launch_description():
    return describe("stock", "mecanum_drive_node.py")
