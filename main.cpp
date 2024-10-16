#include <stdio.h>
#include <math.h>
#include "Kinematics.h"

int main() {
  Kinematics kinematics;
  std::array<double, 3> motor_angles = kinematics.setPosition(20*pi/180, 20*pi/180);
  printf("%f, %f, %f\n", motor_angles[0], motor_angles[1], motor_angles[2]);
}