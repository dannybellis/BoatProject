#Authors: Fiona Shyne and London Lowmanstone
#!/usr/bin/env python 

boat = Boat(40, 20)
# start the ros node
rospy.init_node('simple_controller', anonymous=True)
rate = rospy.Rate(10) # 10hz
initial_flag = 1 
while not rospy.is_shutdown():

    boat.drive()
    rate.sleep()
    
