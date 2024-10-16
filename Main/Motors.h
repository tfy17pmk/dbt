#ifndef MOTORS_H
#define MOTORS_H

#include "Arduino.h"

class Motors {
public:
    // Constructor to initialize motors with mode, direction, and step pins
    Motors(int modePins[], int dirPins[], int stepPins[]);
    
    void initial_position();
    void set_angle(float goal_angles[3]);
    void clean_up();

private:
    // Member variables for motor control    
    int MODE[3];
    int DIR[3];
    int STEP[3];
    float current_angles[3];
    float relative_angles[3];
    float required_steps[3];
    unsigned long rotation_times[3];
    int step_direction[3];

    int RESOLUTION[3] = {1,0,1}; // Resolution for 1/32 microstepping 
    float degree_per_step = 1.8/32.0; // Set degree per step;
    int PWM_frequency = 8000; // Set PWM frequency;
    int PWM_duty = 128; // Set default PWM value
};

#endif // MOTORS_H
