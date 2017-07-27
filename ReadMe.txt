Boat project mission: 
  collect an orange pingpong ball at a gps location using robotic boats and intake system 

Where to find stuff on the vm 
  1.programs to run the robot are located in rsn/umn-ros-pkg/rsn/carpMonitorinh/Bridge/nodes/ #notes on how to run robot are below
  2.scripts to run the robot from the command line are in rsn/umn-ros-pkg/rsn/carpMonitoring/scripts_cmd/
  3.arduino code for the conveyor belt is in the arduino folder under the home directitory 
  4.arduino code to run the propellor and rudder are located in rsn/umn-ros-pkg/rsn/carpMonitoring/ 
  
important programs 
  located in the node folder is:
    1.lavant_bridge_timer - run before you launch other code 
    2.TargetTracking - main code for ping pong ball project 
    3. boat_cmds -contains functions nessisary to run the boat 
    4. Vision.py -gives position and distance to the orange pingpong ball 
  

OpenCV download
https://pypi.python.org/pypi/opencv-python

Py Version
cp35

cmd command
python - m instll opencv-python

Running code on robot
steps:
 1. Turn on robot and connect to it
 2. From cmd type "roscore&"
 3. Go to directory rsh/umn-ros-pkg/rsn/carpMonitoring/Bridge/nodes/
    (Shortcut "roscd Bridge")
 4. Type "./lavant_bridge_timer.py" then press enter
 5. Open another instence of cmd
 6. Ping robot (ip - 192.168.100.12)
 7. Navigate to rsh/umn-ros-pkg/rsn/carpMonitoring/Bridge/nodes/
    (Shortcut "roscd Bridge")
 8. Run your code with ./Your_codes_name.py

Manualy controling robot
steps:
 1. Turn on robot and connect to it
 2. From cmd type "roscore&"
 3. Go to directory rsh/umn-ros-pkg/rsn/carpMonitoring/Bridge/nodes/
    (Shortcut "roscd Bridge")
 4. Type "./lavant_bridge_timer.py" then press enter
 5. Open another instence of cmd
 6. Ping robot (ip - 192.168.100.12)
 7. Go to directory rsh/umn-ros-pkg/rsn/carpMonitoring/scripts_cmd/
 8. To steer do "rostopic pub -r 10 /motor_cmd/steer std_msgs/Int8 Your_Angle" (Make sure you dont go over 30 or under -30 deg)
    To move do "rostopic pub -r 10 /motor_cmd/propeller std_msgs/Int Your_Speed"
