# ohm_odometry

Lab session *Kinematics and odometry* (180 minutes) on the
[`ir-mecanum-lab`](https://github.com/christianpfitzner/ir-mecanum-lab) simulator: students write the
kinematics of a differential drive and a mecanum drive and compute odometry from the wheel encoders,
in the empty hall `open`, against the true pose. Practicum *Intelligente Robotik*.

The repository directory is `ohm-odometry`, the ROS package is `ohm_odometry`. The simulator is a
separate checkout and must have the differential drive (`--variant diff`) and the wheel encoders
(`/<robot>/joint_states`, `sensor_msgs/JointState` as on a real robot with `ros2_control`): odometry is
computed from the measured wheel angles, so the lab needs a topic that carries them.

## Layout

| path | what | handed out |
|---|---|---|
| `docs/odometry.tex`, `docs/odometry.pdf` | the handout (`make -C docs`) | yes |
| `student/diff_drive_node.py` | part A: ROS 2 node of the differential drive, four TODOs | yes |
| `student/mecanum_drive_node.py` | part B: ROS 2 node of the mecanum drive, four TODOs | yes |
| `student/square_node.py`, `student/goto_node.py` | extra tasks E1 and E2: the students' node driven by a controller instead of the keyboard | yes |
| `launch/diff_demo.launch.py`, `launch/mecanum_demo.launch.py` | task 0: the simulator with its own kinematics, the keys drive | yes |
| `launch/diff.launch.py`, `launch/mecanum.launch.py` | tasks 1-4: the simulator waits for the wheel speeds of the students' node | yes |
| `config/lab_odometry.json`, `config/lab_odometry_demo.json` | hall `open`, encoders and truth on, GPS off; `passthrough` off / on | yes |
| `ohm_odometry/` | finding the simulator (`paths.py`), the launch logic (`launching.py`) | — |
| `test/` | the teaching team's tests | — |

The students change four places per node: the topic names (TODO 1, found with `ros2 topic list` and
`ros2 topic info -v`), the inverse kinematics (2), the forward kinematics (3) and the odometry step (4).
Subscriptions, publishers and reading and writing the messages are given. The handout repeats the
equations of the lecture script with their numbers (1.27-1.30, 1.39, 1.40) and adds the odometry step
of the mecanum drive and two optional extra tasks (square by odometry, drive to a point).

The reference solution is not in this repository. It lives in the separate repository
`ohm-odometry-solutions` of the teaching team.

## Setup

Both repositories side by side in one workspace:

```bash
cd ~/ros2_ws/src
```

```bash
git clone git@github.com:christianpfitzner/ir-mecanum-lab.git
```

Then build both with `--symlink-install`, so `ros2 run` starts the node file the students edit and
not a copy of it:

```bash
cd ~/ros2_ws && colcon build --symlink-install --packages-select mecanum_lab_interfaces mecanum_lab ohm_odometry
```

```bash
source ~/ros2_ws/install/setup.bash
```

The simulator is found in this order (`ohm_odometry/paths.py`): `MECANUM_LAB=<checkout>`, a checkout
next door (`../ir-mecanum-lab` or `../mecanum-lab`), the installed `mecanum_lab`. A checkout wins over
an install because a stale build without the differential drive is the commoner mistake.

## Run

Task 0, the finished robot — the keys drive through the simulator's own kinematics:

```bash
ros2 launch ohm_odometry diff_demo.launch.py
```

From task 1 on, the simulator without its own kinematics: the robot stands until the students' node
sends wheel speeds, and drives wrong when their kinematics is wrong (part B: `mecanum.launch.py`):

```bash
ros2 launch ohm_odometry diff.launch.py
```

The students' node, in a second one (part B: `mecanum_drive_node.py`):

```bash
ros2 run ohm_odometry diff_drive_node.py
```

Until TODO 1 is done the node stops with one line saying so. Launch arguments: `robot:=`, `rviz:=`,
`headless:=`, `seconds:=`.

## Tests (teaching team)

```bash
python3 -m pytest test -q
```

The templates stop cleanly until the topics are filled in, the launch files start only the simulator,
and only the demo config lets the keys drive. Use a ROS domain of your own (`ROS_DOMAIN_ID=…`) when a
simulator runs on the same machine.
