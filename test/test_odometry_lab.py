"""Tests of the lab repository: templates, launch files and configs fit the simulator next door.

The tests of the reference solution live with the solution, in the separate repository
`ohm-odometry-solutions`.

    python3 -m pytest test -q          (in a terminal with ROS 2 sourced)
"""
import importlib.util
import math
import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from ohm_odometry import paths                                 # noqa: E402

paths.use_simulator()
pytest.importorskip("rclpy")
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")


def load(rel):
    spec = importlib.util.spec_from_file_location(rel.replace("/", "_")[:-3], os.path.join(ROOT, rel))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize("node", ["diff_drive_node.py", "mecanum_drive_node.py", "square_node.py",
                                  "goto_node.py"])
def test_the_template_stops_with_one_line_until_the_topics_are_filled_in(node, capsys):
    sys.path.insert(0, os.path.join(ROOT, "student"))   # the extra nodes import the drive nodes
    student = load(f"student/{node}")
    assert getattr(student, "base", student).TOPIC_ENCODERS == "TODO"
    student.main()
    assert "TODO 1" in capsys.readouterr().out
    assert os.access(os.path.join(ROOT, "student", node), os.X_OK)    # `ros2 run` needs the bit


@pytest.mark.parametrize("name", ["diff", "mecanum", "diff_demo", "mecanum_demo"])
def test_launch_files_start_the_simulator_only(name):
    pytest.importorskip("launch")
    description = load(f"launch/{name}.launch.py").generate_launch_description()
    args = {a.name for a in description.entities if hasattr(a, "default_value")}
    assert args == {"robot", "rviz", "headless", "seconds"}


def test_only_the_demo_lets_the_keys_drive():
    from mecanum_lab.types import load_config
    assert load_config(paths.lab_file("config", "lab_odometry_demo.json"))["passthrough"] is True
    assert load_config(paths.lab_file("config", "lab_odometry.json"))["passthrough"] is False
