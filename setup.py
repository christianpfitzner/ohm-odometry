"""The lab as a ROS 2 package: `colcon build --symlink-install`, then `ros2 launch ohm_odometry …`.

The two student nodes are installed as executables of the package, so `ros2 run ohm_odometry
diff_drive_node.py` starts them. Build with `--symlink-install`: the installed node is then a symlink to the
file a group edits.
"""
from glob import glob
import os

from setuptools import setup

PACKAGE = "ohm_odometry"

setup(
    name=PACKAGE,
    version="0.1.0",
    description="Lab 'Kinematics and odometry' for the mecanum-lab simulator",
    author="Praktikum Intelligente Robotik",
    license="MIT",
    python_requires=">=3.10",
    packages=[PACKAGE],
    data_files=[
        (os.path.join("share", "ament_index", "resource_index", "packages"), ["resource/" + PACKAGE]),
        (os.path.join("share", PACKAGE), ["package.xml"]),
        (os.path.join("share", PACKAGE, "launch"), glob("launch/*.py")),
        (os.path.join("share", PACKAGE, "config"), glob("config/*.json")),
        # The two nodes the students write, as executables: `ros2 run ohm_odometry diff_drive_node.py`.
        # With --symlink-install these are symlinks to student/, so `ros2 run` starts the edited file.
        (os.path.join("lib", PACKAGE), glob("student/*_node.py")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
)
