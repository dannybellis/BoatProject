/* 
 * When meassage recieved turn conveyor on and lower it 
 */

#include <ros.h>
#include <std_msgs/Bool.h>
#include <Servo.h>

ros::NodeHandle  nh;
const int lower_pin = 13; // pin that raises the conveyor
const int on_pin = 15; // pin that spins the conveyor
bool lowered_msg; 
bool on_msg;
Servo on_servo;
Servo lower_servo;  
int on_pos = 120;
int off_pos = 90; 
int lowered_pos = 135; 
int lowered_off_pos = 90;
int raised_pos = 45;
int wait_time = 100; //miliseconds to wait before turning lower motor off 



void conveyor_lower( const std_msgs::Bool& msg){
  lowered_msg = msg.data;
  //lower conveyor belt
  if (lowered_msg){
      //lower conveyor belt 
      lower_servo.write(lowered_pos);
      delay(wait_time); 
      lower_servo.write(lowered_off_pos);
  }
  else{
      //raise conveyor belt
      lower_servo.write(raised_pos);
      delay(wait_time); 
      lower_servo.write(lowered_off_pos);
  }
}

void conveyor_on( const std_msgs::Bool& msg){
  on_msg = msg.data;
  //lower conveyor belt
  if (on_msg){
      //turn conveyor on
      on_servo.write(on_pos);
      
  }
  else{
      //turn coneyor off 
      on_servo.write(off_pos);
  }
} 


ros::Subscriber<std_msgs::Bool> lower("motor_cmd/conveyor_lower", &conveyor_lower);
ros::Subscriber<std_msgs::Bool> on("motor_cmd/conveyor_on", &conveyor_on);




void setup()
{ 

  on_servo.attach(on_pin);
  lower_servo.attach(lower_pin);
  nh.initNode();
  nh.subscribe(lower);
  nh.subscribe(on);
}

void loop()
{  
  nh.spinOnce();
  delay(1);
}
