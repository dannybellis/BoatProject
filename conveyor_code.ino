/* 
 * When meassage recieved turn conveyor on and lower it 
 */

#include <ros.h>
#include <std_msgs/Bool.h>

ros::NodeHandle  nh;
const int lower_pin = 13; // pin that raises the conveyor
const int on_pin = 15; // pin that spins the conveyor
bool lowered_msg; 
bool on_msg;


void conveyor_lower( const std_msgs::Bool& msg){
  lowered_msg = msg.data;
  //lower conveyor belt
  if (lowered_msg){
      //lower conveyor belt 
  }
  else{
      //raise conveyor belt
  }
}

void conveyor_on( const std_msgs::Bool& msg){
  on_msg = msg.data;
  //lower conveyor belt
  if (on_msg){
      //turn conveyor on
  }
  else{
      //turn coneyor off 
  }
} 


ros::Subscriber<std_msgs::Bool> lower("motor_cmd/conveyor_lower", &conveyor_lower);
ros::Subscriber<std_msgs::Bool> on("motor_cmd/conveyor_on", &conveyor_on);




void setup()
{ 

  pinMode(lower_pin, OUTPUT);
  pinMode(on_pin, OUTPUT);
  nh.initNode();
  nh.subscribe(lower);
  nh.subscribe(on);
}

void loop()
{  
  nh.spinOnce();
  delay(1);
}
