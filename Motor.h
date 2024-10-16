#ifndef MOTORS_H
#define MOTORS_H

#include <Arduino.h>

class Motors {
public:
    // Constructor to initialize motors with mode, direction, and step pins
    Motors(int modePins[3], int dirPins[3], int stepPins[3]);
    
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
    float degree_per_step;
    int PWM_frequency;
    int PWM;
};

#endif // MOTORS_H
