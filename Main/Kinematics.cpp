#include "Arduino.h"
#include <stdio.h>
#include <array>
#include <math.h>
#include "Kinematics.h"

#define pi 3.1415926535

Kinematics::Kinematics() {
}
std::array<double, 3> Kinematics::inverseKinematics(double *normal_vector, double height) {
  double base_to_servo_length = _lengths[0];
  double arm_1_length = _lengths[1];
  double arm_2_length = _lengths[2];
  double platform_radius = _lengths[3];

  // Set reference height for arms (A-E are intermediate variables for simplified calculations)
  double A = (base_to_servo_length + arm_1_length) / height;
  double B = (pow(height,2) + pow(arm_2_length,2) - pow(base_to_servo_length + arm_1_length,2) - pow(platform_radius,2)) / (2*height);
  double C = pow(A,2) + 1;
  double D = 2 * (A * B - (base_to_servo_length + arm_1_length));
  double E = pow(B,2) + pow(base_to_servo_length + arm_1_length,2) - pow(arm_2_length,2);

  //printf("%f, %f, %f, %f, %f\n", A, B, C, D, E);

  double Pmx = (-D + sqrt(pow(D,2) - 4 * C * E)) / (2 * C);
  double Pmz = sqrt(pow(arm_2_length,2) - pow(Pmx,2) + 2 * (base_to_servo_length + arm_1_length) * Pmx - pow(base_to_servo_length + arm_1_length,2));
  
  //printf("%f, %f\n", Pmx, Pmz);

  //""" --------------------------------------- FIRST ARM --------------------------------------- """
  // Mounting point on the platform
  double arm_1_x_mount = normal_vector[2] * platform_radius / sqrt(pow(normal_vector[0],2) + pow(normal_vector[2],2));
  double arm_1_y_mount = 0;
  double arm_1_z_mount = height - normal_vector[0] * platform_radius / sqrt(pow(normal_vector[0],2) + pow(normal_vector[2],2));
  double arm_1_mount_array[3] = {arm_1_x_mount, arm_1_y_mount, arm_1_z_mount};


  //printf("%f, %f, %f\n", arm_1_x_mount, arm_1_y_mount, arm_1_z_mount);

  // Define knee coordinates (A_1-E_1 are intermediate variables for simplified calculations)
  double A_1 = (base_to_servo_length - arm_1_mount_array[0]) / arm_1_mount_array[2];
  double B_1 = (pow(arm_1_mount_array[0],2) + pow(arm_1_mount_array[2],2) + pow(arm_1_length,2) - pow(base_to_servo_length,2) - pow(arm_2_length,2)) / (2 * arm_1_mount_array[2]);
  double C_1 = pow(A_1,2) + 1;
  double D_1 = 2 * (A_1 * B_1 - base_to_servo_length);
  double E_1 = pow(B_1,2) + pow(base_to_servo_length,2) - pow(arm_1_length,2);

  //printf("%f, %f, %f, %f, %f\n", A_1, B_1, C_1, D_1, E_1);

  // Coordinates of knee
  double arm_1_x_knee = (-D_1 + sqrt(pow(D_1,2) - 4 * C_1 * E_1)) / (2 * C_1);
  double arm_1_y_knee = 0;
  double arm_1_z_knee = sqrt(pow(arm_1_length,2) - pow(arm_1_x_knee - base_to_servo_length,2));

  if (arm_1_z_mount < Pmz) {
    arm_1_z_knee = -arm_1_z_knee;
  }

  //printf("%f, %f, %f\n", arm_1_x_knee, arm_1_y_knee, arm_1_z_knee);
  
  double arm_1_knee_array[3] = {arm_1_x_knee, arm_1_y_knee, arm_1_z_knee};

  double arm_1_costheta = (arm_1_knee_array[0] - base_to_servo_length);
  double arm_1_sintheta = (arm_1_knee_array[2]);

  //printf("%f, %f\n", arm_1_costheta, arm_1_sintheta);

  double arm_1_theta = pi/2 - atan2(arm_1_costheta, arm_1_sintheta);

  //printf("%f\n", arm_1_theta);

  //""" --------------------------------------- SECOND ARM --------------------------------------- """
  // Mounting point on the platform
  double arm_2_x_mount = (-platform_radius * normal_vector[2]) / sqrt(pow(normal_vector[0],2) + 3 * pow(normal_vector[1],2) + 4 * pow(normal_vector[2],2) + 2 * sqrt(3) * normal_vector[0] * normal_vector[1]);
  double arm_2_y_mount = -(sqrt(3) * platform_radius * normal_vector[2]) / sqrt(pow(normal_vector[0],2) + 3 * pow(normal_vector[1],2) + 4 * pow(normal_vector[2],2) + 2 * sqrt(3) * normal_vector[0] * normal_vector[1]);
  double arm_2_z_mount = height + (platform_radius * (sqrt(3) * normal_vector[1] + normal_vector[0])) / sqrt(pow(normal_vector[0],2) + 3 * pow(normal_vector[1],2) + 4 * pow(normal_vector[2],2) + 2 * sqrt(3) * normal_vector[0] * normal_vector[1]);
  double arm_2_mount_array[3] = {arm_2_x_mount, arm_2_y_mount, arm_2_z_mount};

  // Define knee coordinates (A_2-E_2 are intermediate variables for simplified calculations)
  double A_2 = -(arm_2_mount_array[0] + sqrt(3) * arm_2_mount_array[1] + 2 * base_to_servo_length) / arm_2_mount_array[2];
  double B_2 = (pow(arm_2_mount_array[0],2) + pow(arm_2_mount_array[1],2) + pow(arm_2_mount_array[2],2) + pow(arm_1_length,2) - pow(base_to_servo_length,2) - pow(arm_2_length,2)) / (2 * arm_2_mount_array[2]);
  double C_2 = pow(A_2,2) + 4;
  double D_2 = 2 * A_2 * B_2 + 4 * base_to_servo_length;
  double E_2 = pow(B_2,2) + pow(base_to_servo_length,2) - pow(arm_1_length,2);

  double arm_2_x_knee = (-D_2 - sqrt(pow(D_2,2) - 4 * C_2 * E_2)) / (2 * C_2);
  double arm_2_y_knee = sqrt(3) * arm_2_x_knee;
  double arm_2_z_knee = sqrt(pow(arm_1_length,2) - 4 * pow(arm_2_x_knee,2) - 4 * base_to_servo_length * arm_2_x_knee - pow(base_to_servo_length,2));

  if (arm_2_z_mount < Pmz) {
    arm_2_z_knee = -arm_2_z_knee;
  }
  double arm_2_knee_array[3] = {arm_2_x_knee, arm_2_y_knee, arm_2_z_knee};

  double arm_2_theta = pi/2 - atan2(sqrt(pow(arm_2_knee_array[0],2) + pow(arm_2_knee_array[1],2)) - base_to_servo_length, arm_2_knee_array[2]);

  //printf("%f\n", arm_2_theta);

  //""" --------------------------------------- THIRD ARM --------------------------------------- """
  // Mounting point on the platform
  double arm_3_x_mount = (-platform_radius * normal_vector[2]) / sqrt(pow(normal_vector[0],2) + 3 * pow(normal_vector[1],2) + 4 * pow(normal_vector[2],2) - 2 * sqrt(3) * normal_vector[0] * normal_vector[1]);
  double arm_3_y_mount = (sqrt(3) * platform_radius * normal_vector[2]) / sqrt(pow(normal_vector[0],2) + 3 * pow(normal_vector[1],2) + 4 * pow(normal_vector[2],2) - 2 * sqrt(3) * normal_vector[0] * normal_vector[1]);
  double arm_3_z_mount = height + (platform_radius * (-sqrt(3) * normal_vector[1] + normal_vector[0])) / sqrt(pow(normal_vector[0],2) + 3 * pow(normal_vector[1],2) + 4 * pow(normal_vector[2],2) - 2 * sqrt(3) * normal_vector[0] * normal_vector[1]);
  double arm_3_mount_array[3] = {arm_3_x_mount, arm_3_y_mount, arm_3_z_mount};
  
  // Define knee coordinates (A_3-E_3 are intermediate variables for simplified calculations)
  double A_3 = -(arm_3_mount_array[0] - sqrt(3) * arm_3_mount_array[1] + 2 * base_to_servo_length) / arm_3_mount_array[2];
  double B_3 = (pow(arm_3_mount_array[0],2) + pow(arm_3_mount_array[1],2) + pow(arm_3_mount_array[2],2) + pow(arm_1_length,2) - pow(base_to_servo_length,2) - pow(arm_2_length,2)) / (2 * arm_3_mount_array[2]);
  double C_3 = pow(A_3,2) + 4;
  double D_3 = 2 * A_3 * B_3 + 4 * base_to_servo_length;
  double E_3 = pow(B_3,2) + pow(base_to_servo_length,2) - pow(arm_1_length,2);
  /*
  Serial.println(A_3);
  Serial.println(B_3);
  Serial.println(C_3);
  Serial.println(D_3);
  Serial.println(E_3);
  */
  double arm_3_x_knee = (-D_3 - sqrt(pow(D_3,2) - 4 * C_3 * E_3)) / (2 * C_3); 
  double arm_3_y_knee = sqrt(3) * arm_3_x_knee;
  double arm_3_z_knee = sqrt(pow(arm_1_length,2) - 4 * pow(arm_3_x_knee,2) - 4 * base_to_servo_length * arm_3_x_knee - pow(base_to_servo_length,2));
  /*
  Serial.println(arm_3_x_knee);
  Serial.println(arm_3_y_knee);
  Serial.println(arm_3_z_knee);
  */
  if (arm_3_z_mount < Pmz) {
    arm_3_z_knee = -arm_3_z_knee;
  }
  double arm_3_knee_array[3] = {arm_3_x_knee, arm_3_y_knee, arm_3_z_knee};

  double arm_3_theta = pi/2 - atan2(sqrt(pow(arm_3_knee_array[0],2) + pow(arm_3_knee_array[1],2)) - base_to_servo_length, arm_3_knee_array[2]);

  //""" ---------------------------------------------------------------------------------------- """

  // Return the three calculated theta values for the arms
  std::array<double, 3> thetas = {arm_1_theta, arm_2_theta, arm_3_theta};

  return thetas;
}

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
      //Serial.println(_y / _mag) + acos((pow(_mag, 2) + pow(_f, 2) - pow(_g, 2)) / (2 * _mag * _f));
      _clamped = (pow(_mag, 2) + pow(_f, 2) - pow(_g, 2)) / (2 * _mag * _f);
      //_clamped = constrain(_clamped, -1, 1);
      _angle = acos(_y / _mag) + acos(_clamped);
      break;
    case leg2:  //Leg B
      _x = (sqrt(3) / 2) * (_e * (1 - (pow(nx, 2) + sqrt(3) * nx * ny) / (nz + 1)) - _d);
      _y = _x / sqrt(3);
      _z = hz - (_e / 2) * (sqrt(3) * nx + ny);
      _mag = sqrt(pow(_x, 2) + pow(_y, 2) + pow(_z, 2));
      _clamped = (pow(_mag, 2) + pow(_f, 2) - pow(_g, 2)) / (2 * _mag * _f);
      //_clamped = constrain(_clamped, -1, 1);
      _angle = acos((sqrt(3) * _x + _y) / (-2 * _mag)) + acos(_clamped);
      break;
    case leg3:  //Leg C
      _x = (sqrt(3) / 2) * (_d - _e * (1 - (pow(nx, 2) - sqrt(3) * nx * ny) / (nz + 1)));
      _y = -_x / sqrt(3);
      _z = hz + (_e / 2) * (sqrt(3) * nx - ny);
      _mag = sqrt(pow(_x, 2) + pow(_y, 2) + pow(_z, 2));
      _clamped = (pow(_mag, 2) + pow(_f, 2) - pow(_g, 2)) / (2 * _mag * _f);
      //_clamped = constrain(_clamped, -1, 1);
      _angle = acos((sqrt(3) * _x - _y) / (2 * _mag)) + acos(_clamped);
      break;
  }
  return (_angle * (180 / pi));  //converts angle to degrees and returns the value
}
std::array<double, 3> Kinematics::setPosition(double theta, double phi) {
  // Set boundaries for table angles
  if (theta > _maxTheta) {
    theta = _maxTheta;
  }
  else if (theta < _minTheta) {
    theta = _minTheta;
  }

  if (phi > _maxPhi) {
    phi = _maxPhi;
  }
  else if (phi < _minPhi) {
    phi = _minPhi;
  }


  // Calculate x, y, z component of normal from angles theta and phi
  double normal_vector_x = cos(pi/2 - theta);
  double normal_vector_y = cos(pi/2 - phi);
  //Serial.println(-cos(pi/2 - theta));
  //Serial.println(-cos(pi/2 - theta));
  double normal_vector_z = sqrt(1 - pow(normal_vector_x,2) - pow(normal_vector_y,2));

  double normal_vector[3] = {normal_vector_x, normal_vector_y, normal_vector_z};
  // motor angles in absolut degrees
  // = inverseKinematics(normal_vector, _initialPosition[2]);

  motor_angles[0] = thetas(leg1, _height, normal_vector_x, normal_vector_y); // return degree
  motor_angles[1] = thetas(leg2, _height, normal_vector_x, normal_vector_y);
  motor_angles[2] = thetas(leg3, _height, normal_vector_x, normal_vector_y);

  /*motor_angles[0] = motor_angles[0]*(180/pi);
  motor_angles[1] = motor_angles[1]*(180/pi);
  motor_angles[2] = motor_angles[2]*(180/pi);*/

  //printf("%f, %f, %f\n", motor_angles[0], motor_angles[1], motor_angles[2]);

  return motor_angles;
}