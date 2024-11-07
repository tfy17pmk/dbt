#ifndef Kinematics_h
#define Kinematics_h

#include "Arduino.h"
#include <math.h>
#include <array>

#define pi 3.1415926535

//constants
#define leg1 0
#define leg2 1
#define leg3 2

class Kinematics {
public:
  Kinematics();
  std::array<double, 3> setPosition(double normal_vector_x, double normal_vector_y, double _height);
  double thetas(int leg, double hz, double nx, double ny);

private:
  std::array<double, 3> motor_angles = {0, 0, 0};
  double _maxHeight = 0.27;
  double _height = 15;
  double _minHeight = 0.1;
  double _max_normal_x = 0.15;
  double _min_normal_x = -0.15;
  double _max_normal_y = 0.15;
  double _min_normal_y = -0.15;

  double _d = 7.5;  //distance from the center of the base to any of its corners
  double _e = 22;  //22distance from the center of the platform to any of its corners
  double _f = 9;  //length of link #1
  double _g = 15;  //length of link #2

  //Calculation Variables
  double _x, _y, _z;   //generic variables for the components of legs A, B, and C
  double _mag;       //generic magnitude of the leg vector
  double _angle;     //generic angle for legs A, B, and C
  double nmag, nz;  //magnitude and z component of the normal vector
  double _clamped;
};
#endif
