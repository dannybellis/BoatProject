Boat project mission: 
  collect an orange pingpong ball at a gps location using robotic boats and intake system 

Where to find stuff on the vm 
  programs to run the robot are located in rsn/umn-ros-pkg/rsn/carpMonitorinh/Bridge/nodes/ #notes on how to run robot are below
  scripts to run the robot from the command line are in rsn/umn-ros-pkg/rsn/carpMonitoring/scripts_cmd/
  arduino code for the conveyor belt is in the arduino folder under the home directitory 
  arduino code to run the propellor and rudder are located in rsn/umn-ros-pkg/rsn/carpMonitoring/ 
  
important programs (located in the node folder)
    lavant_bridge_timer - run before you launch other code 
    TargetTracking - main code for ping pong ball project 
    boat_cmds -contains functions nessisary to run the boat 
    Vision.py -gives position and distance to the orange pingpong ball 

basic ros commands (run in the command line) 
   roscore& - initialize ros 
   roscd - go to import ros place (like Bridge) 
   rostopic list -get a list of current ros topics 
   rostopic echo -prints messages being sent to ros topics
  

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
    
    
Setup arduino 
  1.make sure arduino is connected to vm (use this site to get the serial port setup http://joequery.me/guides/arduino-ubuntu-virtualbox-windows-host/) 
  2. open arduino ide and upload your code 
  3. type roscore& into terminal 
  4. in a new tab enter this into the command line rosrun rosserial_python serial_node.py /dev/ttyACM0 -- make sure this last part is where your arduino is plugges in 

