/*
 * This file is part of the ball ballancing robot.
 *
 * Developed for Curiosum during the design bulid test course, fall 2024 by 
 * project group 11.
 *
 * date: 4/12-2024
 */
#include "Arduino.h"
#include <stdio.h>
#include <array>
#include <math.h>
#include "Kinematics.h"

#define pi 3.1415926535

Kinematics::Kinematics() {
}

/*
* Description: Calculates motor angles from the normal vector of the table
*
* Input: which leg, height of table, normal vector component in x and y direction. 
*
* Output: motor angle in degrees
*/
double Kinematics::thetas(int leg, double hz, double nx, double ny) {

    //create unit normal vector
    nmag = sqrt(pow(nx, 2) + pow(ny, 2) + 1);  //magnitude of the normal vector
    nx /= nmag;
    ny /= nmag;
    nz = 1 / nmag;

    switch (leg) {
    case leg1:  //Leg A
      _y = _d + (_e / 2) * (1 - (pow(nx, 2) + 3 * pow(nz, 2) + 3 * nz) / (nz + 1 - pow(nx, 2) + (pow(nx, 4) - 3 * pow(nx, 2) * pow(ny, 2)) / ((nz + 1) * (nz + 1 - pow(nx, 2)))));
      _z = hz + _e * ny;
      _mag = sqrt(pow(_y, 2) + pow(_z, 2));
      _angle = acos(_y / _mag) + acos((pow(_mag, 2) + pow(_f, 2) - pow(_g, 2)) / (2 * _mag * _f));
      break;
    case leg2:  //Leg B
      _x = (sqrt(3) / 2) * (_e * (1 - (pow(nx, 2) + sqrt(3) * nx * ny) / (nz + 1)) - _d);
      _y = _x / sqrt(3);
      _z = hz - (_e / 2) * (sqrt(3) * nx + ny);
      _mag = sqrt(pow(_x, 2) + pow(_y, 2) + pow(_z, 2));
      _angle = acos((sqrt(3) * _x + _y) / (-2 * _mag)) + acos((pow(_mag, 2) + pow(_f, 2) - pow(_g, 2)) / (2 * _mag * _f));
      break;
    case leg3:  //Leg C
      _x = (sqrt(3) / 2) * (_d - _e * (1 - (pow(nx, 2) - sqrt(3) * nx * ny) / (nz + 1)));
      _y = -_x / sqrt(3);
      _z = hz + (_e / 2) * (sqrt(3) * nx - ny);
      _mag = sqrt(pow(_x, 2) + pow(_y, 2) + pow(_z, 2));
      _angle = acos((sqrt(3) * _x - _y) / (2 * _mag)) + acos((pow(_mag, 2) + pow(_f, 2) - pow(_g, 2)) / (2 * _mag * _f));
      break;
  }
  return (_angle * (180 / pi));  //converts angle to degrees and returns the value
}
/*
* Description: Constrain normal vector component in x and y direction and compute motor angles 
*
* Input: normal vector component in x and y direction and the height of the table
*
* Output: motor angles in degrees
*/
std::array<double, 3> Kinematics::setPosition(double normal_vector_x, double normal_vector_y, double _height) {
  // Set boundaries for table angles
  if (normal_vector_x > _max_normal_x) {
    normal_vector_x = _max_normal_x;
  }
  else if (normal_vector_x < _min_normal_x) {
    normal_vector_x = _min_normal_x;
  }

  if (normal_vector_y > _max_normal_y) {
    normal_vector_y = _max_normal_y;
  }
  else if (normal_vector_y < _min_normal_y) {
    normal_vector_y = _min_normal_y;
  }
  

  
  motor_angles[0] = thetas(leg1, _height, normal_vector_x, normal_vector_y); // return degree
  motor_angles[1] = thetas(leg2, _height, normal_vector_x, normal_vector_y);
  motor_angles[2] = thetas(leg3, _height, normal_vector_x, normal_vector_y);


  return motor_angles;
}