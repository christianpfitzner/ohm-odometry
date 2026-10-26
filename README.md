# ohm_odometry

Lab *Kinematics and odometry* for the simulator
[ir-mecanum-lab](https://github.com/christianpfitzner/ir-mecanum-lab). Handout: `docs/odometry.pdf`.

## Install

Students: fork this repository first and clone your fork instead.

```bash
cd ~/ros2_ws/src
git clone git@github.com:christianpfitzner/ir-mecanum-lab.git
git clone git@github.com:christianpfitzner/ohm-odometry.git
cd ~/ros2_ws
colcon build --symlink-install --packages-select mecanum_lab_interfaces mecanum_lab ohm_odometry
source install/setup.bash
```

`--symlink-install` matters: `ros2 run` then starts the files in `student/` that you edit.

## Run

| command | what |
|---|---|
| `ros2 launch ohm_odometry diff_demo.launch.py` | task 0: finished robot, the keys drive |
| `ros2 launch ohm_odometry diff.launch.py` | tasks 1–4: the robot only moves with your node |
| `ros2 run ohm_odometry diff_drive_node.py` | your node (template `student/diff_drive_node.py`) |
| `ros2 run ohm_odometry square_node.py` | extra task E1 |
| `ros2 run ohm_odometry goto_node.py` | extra task E2 |

For the mecanum drive use `mecanum_demo.launch.py`, `mecanum.launch.py` and `mecanum_drive_node.py`.

Launch arguments: `robot:=`, `rviz:=`, `headless:=`, `seconds:=`. If the simulator is not found, set
`MECANUM_LAB=<path to the checkout>`.

## Tests

```bash
python3 -m pytest test -q
```
