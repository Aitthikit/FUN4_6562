
# FUN4 6562

FUN4: Hello world 


## System architecture

![alt text](https://github.com/aitthikit/FUN4_6562/blob/main/System.png?raw=true)
![alt text](https://github.com/aitthikit/FUN4_6562/blob/main/rvizcontrol.png?raw=true)


## Package requirement
Please Install this follower Package on your environment
- [Teleop_twist_keyboard for control manipulator](https://github.com/rohbotics/ros2_teleop_keyboard)
But it also have this Package in this git


## Setup environment
1. Clone workspace :
```sh
git clone https://github.com/Aitthikit/FUN4_6562.git -b Final
```
2. Navigate to the workspace directory :
```sh
cd FUN4_6562
```
3. Remove build install log(if it have in workspace) :
```sh
rm -rf build/ install/ log/
```
4. Build :
```sh
colcon build
```
5. Source workspace :
```sh
source install/setup.bash
```
## Run
1. Run launch file :
```sh
ros2 launch example_description all_launch.py
```
2. Use service to select mode
```sh
ros2 service call /mode robot_interface/srv/Mode "mode:
  data: 2
point:
  layout:
    dim: []
    data_offset: 0
  data: [0.0,0.0,0.0]
mode_tele:
  data: 1" 
```
- mode 
    - data: 1 = Inverse Pose Kinematics (IPK)
    - data: 2 = Teleoperation
    - data: 3 = Auto
- point (use for point target to mode Inverse Pose Kinematics (IPK))
    - data: [x,y,z] (only float format)
- mode_tele (use for select in mode Auto)
    - data: 1 = Reference to base
    - data: 2 = Reference to end-effector

    like example is select mode Teleoperation and mode_tele Reference to base
3. Interface monitor
```sh
ros2 topic echo /singularity_notify
```
4. Teleop_keyboard to control mode Teleoperation
```sh
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```
## Bugfix
1. Do not forget to close this monitor before service call 
    -   ![alt text](https://github.com/aitthikit/FUN4_6562/blob/main/close.png?raw=true)
2. Do not forget to Source workspace :
```sh
source install/setup.bash
```
    

