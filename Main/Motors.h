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
    void setup_homing();
    void set_angle(float goal_angles[3]);
    void clean_up();
    void home();
    void IRAM_ATTR handleButtonPress1();
    void IRAM_ATTR handleButtonPress2();
    void IRAM_ATTR handleButtonPress3();

    volatile bool _skipPhaseOne1 = false;
    const int _buttonPin1 = 25;    // Button pin (limit switch or homing switch)

    volatile bool _skipPhaseOne2 = false;
    const int _buttonPin2 = 5;    // Button pin (limit switch or homing switch)

    volatile bool _skipPhaseOne3 = false;
    const int _buttonPin3 = 4;    // Button pin (limit switch or homing switch)

    std::array<bool, 3> buttonPressed;

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

    void phase1();
    void phase2(int motor, bool first_time);
    void phase3();

    


};

#endif // MOTORS_H
