#include "Kinematics.h"
#define pi 3.1415926535

Kinematics kinematics;

void setup() {
  Serial.begin(9600);
  float motor_angle_1, motor_angle_2, motor_angle_3 = kinematics.setPosition(20*pi/180, 20*pi/180);
  Serial.println(motor_angle_1);
  Serial.println(motor_angle_2);
  Serial.println(motor_angle_3);
}

void loop() {
  // put your main code here, to run repeatedly:

}
