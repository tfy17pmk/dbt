#ifndef MOTORS_H
#define MOTORS_H

#include "Arduino.h"
#include <AccelStepper.h>
#include <array>

class Motors {
public:
    // Constructor to initialize motors with mode, direction, and step pins
    Motors();
    
    void initial_position();
    std::array<AccelStepper, 3>& setup_accel();
    void set_angle(double goal_angles[3]);
    void clean_up();
    void home();
    void IRAM_ATTR handleButtonPress1();
    void IRAM_ATTR handleButtonPress2();
    void IRAM_ATTR handleButtonPress3();

    //const int _buttonPin1 = 25;    // Button pin (limit switch or homing switch)

    //const int _buttonPin2 = 5;    // Button pin (limit switch or homing switch)

    //const int _buttonPin3 = 4;    // Button pin (limit switch or homing switch)
    std::array<int, 3> buttonPin = {25, 5, 4};
    std::array<bool, 3> buttonPressed;
    std::array<bool, 3> skipPhaseOne;

private:
    // Member variables for motor control

    // Pin setup for motors First column first motor
    int _MODE[3] = {14, 32, 15};
    int _DIR[3] = {19, 27, 13};
    int _STEP[3] = {18, 33, 12};
    std::array<AccelStepper, 3> stepper;
    //AccelStepper stepper2;
    //AccelStepper stepper3;

    float _current_angles[3];
    float _relative_angles[3];
    float _required_steps[3];
    unsigned long _rotation_times[3];
    int _step_direction[3];

    int _RESOLUTION[3] = {1,0,1}; // Resolution for 1/32 microstepping 
    float _degree_per_step = 1.8/32.0; // Set degree per step;
    int _PWM_frequency = 8000; // Set PWM frequency;
    int _PWM_duty = 128; // Set default PWM value
    int _steps = 0;

    void phase1();
    void phase2(int motor, bool first_time);
    void phase3();
    void move_up();

    


};

#endif // MOTORS_H
