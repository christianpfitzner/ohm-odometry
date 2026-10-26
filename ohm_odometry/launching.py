"""What the launch files of this lab start: the simulator in the hall `open`, one robot, nothing else.

`*_demo.launch.py` (task 0): the simulator's own kinematics turns the keys into wheel speeds.
`diff.launch.py`, `mecanum.launch.py`: the robot moves only on the wheel speeds of the students' node,
which they run themselves in a second terminal (`ros2 run ohm_odometry diff_drive_node.py`).

Every launch file is one call of `describe()`, which includes the simulator's own `lab.launch.py`
(repository `ir-mecanum-lab`) with `config/lab_odometry.json` or, for the demo,
`config/lab_odometry_demo.json`. Where the simulator is found: `paths.py`.
"""
import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, LogInfo, OpaqueFunction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

from . import paths

ARGS = [
    ("robot", "muster", "robot name"),
    ("rviz", "auto", "RViz 2 beside the window: auto | true | false"),
    ("headless", "false", "without the window (SDL dummy driver)"),
    ("seconds", "", "end after N s of simulation time (empty = until Ctrl-C)"),
]


def _start(context, variant, node, demo):
    arg = lambda name: LaunchConfiguration(name).perform(context)   # noqa: E731
    simulator = paths.simulator_root()
    config = "lab_odometry_demo.json" if demo else "lab_odometry.json"
    forwarded = {"config": paths.lab_file("config", config), "variant": variant,
                 "robot": arg("robot"), "rviz": arg("rviz"), "headless": arg("headless")}
    if arg("seconds"):
        forwarded["seconds"] = arg("seconds")               # empty means "not typed" over there too
    drive = "differential" if variant == "diff" else "mecanum"
    if demo:
        note = "the simulator's own kinematics drives: click into the window and use the keys"
    else:
        note = (f"the robot moves only on the wheel speeds of a node — start yours in a second "
                f"terminal: ros2 run ohm_odometry {node}")
    return [LogInfo(msg=f"[odometry] {drive} drive '{arg('robot')}' in the hall 'open' "
                        f"(simulator {simulator}): {note}"),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(os.path.join(simulator, "launch", "lab.launch.py")),
                launch_arguments=forwarded.items())]


def describe(variant: str, node: str, demo: bool = False) -> LaunchDescription:
    """The simulator for one drive train: `variant` of the simulator, `node` the one the students run.

    `demo` keeps the simulator's own kinematics (the keys drive); without it the robot waits for the
    wheel speeds of the students' node.
    """
    return LaunchDescription([DeclareLaunchArgument(name, default_value=default, description=text)
                              for name, default, text in ARGS]
                             + [OpaqueFunction(function=_start,
                                               kwargs={"variant": variant, "node": node, "demo": demo})])
