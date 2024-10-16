#ifndef MOTORS_H
#define MOTORS_H

#include "Arduino.h"

class Motors {
public:
    // Constructor to initialize motors with mode, direction, and step pins
    Motors(int modePins[3], int dirPins[3], int stepPins[3]);
    
    void initial_position();
    void set_angle(float goal_angles[3]);
    void clean_up();

private:
    // Member variables for motor control
    int _RESOLUTION[3] = {1,0,1} // Resolution for 1/32 microstepping 
    int _MODE[3];
    int _DIR[3];
    int _STEP[3];
    float _current_angles[3];
    float _relative_angles[3];
    float _required_steps[3];
    unsigned long _rotation_times[3];
    int _step_direction[3];
    float _degree_per_step = 1.8/32.0; // Set degree per step;
    int _PWM_frequency = 8000; // Set PWM frequency;
    int _PWM_duty = 128; // Set default PWM value
};

#endif // MOTORS_H
