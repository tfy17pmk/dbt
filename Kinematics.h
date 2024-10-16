#ifndef Kinematics_h
#define Kinematics_h

#include "Arduino.h"
#include <math.h>
#include <array>

#define pi 3.1415926535

class Kinematics {
public:
  Kinematics();
  std::array<double, 3> inverseKinematics(double *normal_vector, double height);
  std::array<double, 3> setPosition(double theta, double phi);
private:
  double _lengths[4] = {0.04, 0.04, 0.065, 0.065}; // {base to servo height, arm 1 length, arm 2 length, platform radius}
  double _initialPosition[3] = {0, 0, 0.0632};
  double _maxHeight = 0.0732;
  double _minHeight = 0.0532;
  double _maxPhi = 20*pi/180;
  double _minPhi = -20*pi/180;
  double _maxTheta = 20*pi/180;
  double _minTheta = -20*pi/180;
};
#endif
