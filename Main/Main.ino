#include "Arduino.h"
#include "Kinematics.h"
#include "Motors.h"
#include <array>  // Include array library

#define pi 3.1415926535

Kinematics kinematics;

  // Pin setup for motors First column first motor
  int mode[3] = {14, 32, 15};
  int direction[3] = {17, 27, 13};
  int step[3] = {21, 33, 12};


void setup() {
  Serial.begin(9600);

  

  Motors motors(mode, direction, step);

  // initialize position
  motors.initial_position(); // Set initial position of the motors


  
  /*
  const int pin_direction_motor1 = 17;
  const int pin_direction_motor2 = 27;
  const int pin_direction_motor3 = 13;

  const int pin_step_motor1 = 21;
  const int pin_step_motor2 = 33;
  const int pin_step_motor3 = 12;

  const int Mode1 = 14;
  const int Mode2 = 32;
  const int Mode3 = 15;
  */
  

  std::array<double, 3> motor_angles = kinematics.setPosition(20*pi/180, 20*pi/180);


  // Print the motor angles
  for (size_t i = 0; i < motor_angles.size(); ++i) {
      Serial.print("Motor angle ");
      Serial.print(i);
      Serial.print(": ");
      Serial.println(motor_angles[i]);
  }

  /*
  Serial.println(motor_angle[0]);
  Serial.println(motor_angle[1]);
  Serial.println(motor_angle[2]);
  */

}

void loop() {
  Motors motors(mode, direction, step);

  float goal_angles[3] = {1, 1, 1};
  motors.set_angle(goal_angles);

  delay(100);
  }

