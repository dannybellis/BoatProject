Everything is in the folder "src"
Note the class to control the conveyor belt is called "Vader" because conveyor sounds like "convader" so we shortened it to "vader".

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